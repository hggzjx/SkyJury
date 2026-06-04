from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import random
import re
import time
import urllib.error
import urllib.request
from copy import deepcopy
from pathlib import Path
from typing import Any


DEFAULT_DATA = "/ssd1/lbh/zjx/skyjury/data/skyjury_bench.json"
DEFAULT_OUTPUT_DIR = "/ssd1/lbh/zjx/skyjury/data/auditor"
DEFAULT_BASE_URL = "https://api.chatanywhere.tech/v1/"
DEFAULT_MODEL = "deepseek-v4-flash"
PERTURBATION_TYPES = ("length", "language")
TARGET_LANGUAGE = "Spanish"

RUBRICS_MARKER = "Rubrics:"
RUBRIC_LINE_RE = re.compile(r"^(\s*-\s+)([^:\n]+?)(:\s*)(.*)$")


SYSTEM_PROMPT = """You create semantic-preserving rubric perturbations for a benchmark.

Return valid JSON only. Do not use Markdown.

Definitions:
- length: substantially expand each rubric definition in English while preserving exactly the original meaning and policy boundary. Write 70-100 English words per rubric when possible, or at least 2.5x the original definition length for very short definitions. Include the scope, boundary conditions, and what should not be inferred, but do not invent new policy criteria.
- language: translate each original rubric definition fully into Spanish. Do not keep English text.

Hard constraints:
- Do not change label ids, label display names, label order, candidate identity, handles, descriptions, or non-rubric text.
- Do not add new moderation categories, examples, severity levels, enforcement actions, or criteria that are not entailed by the original definition.
- Do not remove or narrow any condition from the original definition.
- Keep proper names, URLs, product names, and label identifiers unchanged.
- Output one object for every input rubric id.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build SkyJury rubric perturbation JSONs with an LLM.")
    parser.add_argument("--data", default=DEFAULT_DATA)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--prefix", default=None)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--base-url", default=None)
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=12000)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--retries", type=int, default=8)
    parser.add_argument("--retry-sleep", type=float, default=3.0)
    parser.add_argument("--concurrency", type=int, default=1)
    parser.add_argument("--request-jitter", type=float, default=0.0)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--resume", action="store_true", default=True)
    return parser.parse_args()


def load_local_env() -> None:
    for path in [Path("/ssd1/lbh/zjx/skyjury/.env"), Path("/ssd1/lbh/zjx/skyjury/verifier/.env")]:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_rows(path: str | Path) -> list[dict[str, Any]]:
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError("Input data must be a JSON list.")
    return rows


def extract_rubrics(row: dict[str, Any]) -> list[dict[str, str]]:
    rubric_items: list[dict[str, str]] = []
    for side in ("chosen", "rejected"):
        for candidate_index, candidate in enumerate(row.get(side, [])):
            if RUBRICS_MARKER not in candidate:
                continue
            rubric_block = candidate.split(RUBRICS_MARKER, 1)[1]
            rubric_index = 0
            for line in rubric_block.splitlines():
                match = RUBRIC_LINE_RE.match(line)
                if not match:
                    continue
                _, label_name, _, definition = match.groups()
                definition = definition.strip()
                if not definition:
                    continue
                rubric_items.append(
                    {
                        "id": f"{side}_{candidate_index}_{rubric_index}",
                        "side": side,
                        "candidate_index": str(candidate_index),
                        "label": label_name.strip(),
                        "definition": definition,
                    }
                )
                rubric_index += 1
    return rubric_items


def build_messages(row: dict[str, Any], rubric_items: list[dict[str, str]]) -> list[dict[str, str]]:
    payload = {
        "row_id": row.get("id"),
        "target_language": TARGET_LANGUAGE,
        "rubrics": [
            {
                "id": item["id"],
                "label": item["label"],
                "definition": item["definition"],
            }
            for item in rubric_items
        ],
        "output_schema": [
            {
                "id": "same id as input",
                "length": "expanded English definition",
                "language": "Spanish translation of the original definition",
            }
        ],
    }
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
    ]


def post_chat_completion(
    base_url: str,
    api_key: str,
    model: str,
    messages: list[dict[str, str]],
    temperature: float,
    max_tokens: int,
    timeout: int,
) -> str:
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = json.loads(response.read().decode("utf-8"))
    return body["choices"][0]["message"]["content"]


def parse_json_array(text: str) -> list[dict[str, Any]]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()
    start = cleaned.find("[")
    if start > 0:
        cleaned = cleaned[start:]
    data, _ = json.JSONDecoder().raw_decode(cleaned)
    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON list. Raw prefix: {text[:240]!r}")
    return data


def call_transform(row: dict[str, Any], rubric_items: list[dict[str, str]], args: argparse.Namespace, base_url: str, api_key: str) -> dict[str, dict[str, str]]:
    messages = build_messages(row, rubric_items)
    expected_ids = {item["id"] for item in rubric_items}
    last_error: Exception | None = None
    for attempt in range(args.retries):
        try:
            raw = post_chat_completion(
                base_url=base_url,
                api_key=api_key,
                model=args.model,
                messages=messages,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                timeout=args.timeout,
            )
            parsed = parse_json_array(raw)
            by_id: dict[str, dict[str, str]] = {}
            for item in parsed:
                item_id = str(item.get("id", "")).strip()
                if item_id not in expected_ids:
                    continue
                transformed = {}
                for key in PERTURBATION_TYPES:
                    value = str(item.get(key, "")).strip()
                    if not value:
                        raise ValueError(f"Missing {key} for rubric id {item_id}")
                    transformed[key] = value
                by_id[item_id] = transformed
            missing = expected_ids - set(by_id)
            if missing:
                raise ValueError(f"Missing transformed rubric ids: {sorted(missing)[:5]}")
            return by_id
        except Exception as exc:
            last_error = exc
            print(
                f"row={row.get('id')} attempt {attempt + 1}/{args.retries} failed: "
                f"{type(exc).__name__}: {exc}",
                flush=True,
            )
            if attempt + 1 < args.retries:
                time.sleep(args.retry_sleep * (attempt + 1) + random.uniform(0, args.retry_sleep))
    raise RuntimeError(f"Failed row {row.get('id')} after {args.retries} attempts: {last_error}")


def perturb_candidate(candidate: str, candidate_key: str, transforms: dict[str, dict[str, str]], perturbation_type: str) -> str:
    if RUBRICS_MARKER not in candidate:
        return candidate
    before, rubric_block = candidate.split(RUBRICS_MARKER, 1)
    before = before + RUBRICS_MARKER
    rubric_index = 0
    out_lines = []
    for line in rubric_block.splitlines():
        match = RUBRIC_LINE_RE.match(line)
        if not match:
            out_lines.append(line)
            continue
        prefix, label_name, sep, definition = match.groups()
        if not definition.strip():
            out_lines.append(line)
            continue
        item_id = f"{candidate_key}_{rubric_index}"
        if item_id not in transforms:
            raise KeyError(f"Missing transform for {item_id}")
        out_lines.append(f"{prefix}{label_name}{sep}{transforms[item_id][perturbation_type]}")
        rubric_index += 1
    return before + "\n".join(out_lines)


def apply_transforms_to_row(row: dict[str, Any], transforms: dict[str, dict[str, str]], perturbation_type: str) -> dict[str, Any]:
    out = deepcopy(row)
    for side in ("chosen", "rejected"):
        new_candidates = []
        for candidate_index, candidate in enumerate(out.get(side, [])):
            candidate_key = f"{side}_{candidate_index}"
            new_candidates.append(perturb_candidate(candidate, candidate_key, transforms, perturbation_type))
        out[side] = new_candidates
    return out


def write_json(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")


def transform_row_task(
    index: int,
    total: int,
    row: dict[str, Any],
    args: argparse.Namespace,
    base_url: str,
    api_key: str,
) -> tuple[str, dict[str, Any]]:
    row_id = str(row.get("id"))
    rubric_items = extract_rubrics(row)
    if not rubric_items:
        return row_id, {"transforms": {}}
    print(f"transforming {index}/{total} row={row_id} rubrics={len(rubric_items)}", flush=True)
    if args.request_jitter > 0:
        time.sleep(random.uniform(0, args.request_jitter))
    transforms = call_transform(row, rubric_items, args, base_url, api_key)
    return row_id, {"transforms": transforms}


def main() -> None:
    load_local_env()
    args = parse_args()
    api_key = args.api_key or os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY_CONF")
    base_url = args.base_url or os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_BASE_URL_CONF") or DEFAULT_BASE_URL
    if not api_key:
        raise RuntimeError("Missing API key. Set OPENAI_API_KEY or OPENAI_API_KEY_CONF.")

    data_path = Path(args.data)
    rows = load_rows(data_path)
    if args.limit is not None:
        rows = rows[: args.limit]

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.prefix or data_path.stem
    progress_path = output_dir / f"{prefix}_llm_rubric_perturbation_progress.json"
    base_path = output_dir / f"{prefix}_base.json"
    variant_paths = {
        perturbation: output_dir / f"{prefix}_rubric_{perturbation}.json"
        for perturbation in PERTURBATION_TYPES
    }

    if args.resume and progress_path.exists():
        progress = json.loads(progress_path.read_text(encoding="utf-8"))
    else:
        progress = {"model": args.model, "target_language": TARGET_LANGUAGE, "rows": {}}

    by_id = {row["id"]: row for row in rows}
    pending = [
        (index, row)
        for index, row in enumerate(rows, start=1)
        if str(row.get("id")) not in progress["rows"]
    ]
    print(
        f"rows={len(rows)} pending={len(pending)} concurrency={max(1, args.concurrency)} "
        f"model={args.model}",
        flush=True,
    )
    if pending:
        if args.concurrency <= 1:
            for index, row in pending:
                row_id, result = transform_row_task(index, len(rows), row, args, base_url, api_key)
                progress["rows"][row_id] = result
                progress_path.write_text(json.dumps(progress, indent=2, ensure_ascii=False), encoding="utf-8")
        else:
            with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
                futures = [
                    executor.submit(transform_row_task, index, len(rows), row, args, base_url, api_key)
                    for index, row in pending
                ]
                for completed, future in enumerate(as_completed(futures), start=1):
                    row_id, result = future.result()
                    progress["rows"][row_id] = result
                    progress_path.write_text(json.dumps(progress, indent=2, ensure_ascii=False), encoding="utf-8")
                    print(f"completed {completed}/{len(pending)} row={row_id}", flush=True)

    write_json(base_path, rows)
    variants = {perturbation: [] for perturbation in PERTURBATION_TYPES}
    for row_id in [str(row.get("id")) for row in rows]:
        row = by_id[row_id]
        transforms = progress["rows"][row_id]["transforms"]
        for perturbation in PERTURBATION_TYPES:
            variants[perturbation].append(apply_transforms_to_row(row, transforms, perturbation))

    for perturbation, variant_rows in variants.items():
        write_json(variant_paths[perturbation], variant_rows)

    manifest = {
        "source_data": str(data_path),
        "num_rows": len(rows),
        "model": args.model,
        "target_language": TARGET_LANGUAGE,
        "perturbation_scope": "rubrics_only",
        "semantic_constraint": "length expands definitions without changing meaning; language translates original definitions to Spanish.",
        "base_path": str(base_path),
        "progress_path": str(progress_path),
        "variants": {key: {"path": str(path)} for key, path in variant_paths.items()},
    }
    manifest_path = output_dir / f"{prefix}_rubric_perturbation_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote base: {base_path}", flush=True)
    for perturbation, path in variant_paths.items():
        print(f"wrote {perturbation}: {path}", flush=True)
    print(f"wrote manifest: {manifest_path}", flush=True)


if __name__ == "__main__":
    main()
