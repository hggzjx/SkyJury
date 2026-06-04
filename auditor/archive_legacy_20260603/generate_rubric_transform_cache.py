from __future__ import annotations

import argparse
import json
import os
import re
import time
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_DATA = "/ssd1/lbh/zjx/skyjury/data/skyjury_bench.json"
DEFAULT_OUTPUT = "/ssd1/lbh/zjx/skyjury/data/auditor/rubric_transform_cache_es.json"
DEFAULT_BASE_URL = "https://api.chatanywhere.tech/v1/"
RUBRIC_LINE_RE = re.compile(r"^\s*-\s+([^:\n]+?)(:\s*)(.*)$")


SYSTEM_PROMPT = """You rewrite moderation rubric definitions for a robustness benchmark.

Return valid JSON only. Do not use Markdown.

For each input rubric:
1. expanded_en: Expand the English definition to 2-3 clear sentences while preserving exactly the same semantic scope. Do not add new policy categories, examples, severity levels, actions, or criteria that are not entailed by the original definition.
2. translated_es: Translate the original English definition fully into Spanish. Do not keep the English definition.
3. expanded_translated_es: Translate expanded_en fully into Spanish. Do not keep English text.

The Spanish should be natural international Spanish suitable for a global social platform. Keep proper names, product names, URLs, and label identifiers unchanged.
"""


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate cached rubric expansions/translations.")
    parser.add_argument("--data", default=DEFAULT_DATA)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--model", default=os.getenv("RUBRIC_TRANSFORM_MODEL", "gpt-4o-ca"))
    parser.add_argument("--base-url", default=None)
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--batch-size", type=int, default=20)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=12000)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--retries", type=int, default=6)
    parser.add_argument("--retry-sleep", type=float, default=3.0)
    parser.add_argument("--limit", type=int, default=None)
    return parser.parse_args()


def cache_key(label: str, definition: str) -> str:
    return json.dumps([label.strip(), definition.strip()], ensure_ascii=False, separators=(",", ":"))


def collect_unique_rubrics(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    items: dict[str, dict[str, str]] = {}
    for row in rows:
        for side in ("chosen", "rejected"):
            for candidate in row.get(side, []):
                if "Rubrics:" not in candidate:
                    continue
                block = candidate.split("Rubrics:", 1)[1]
                for line in block.splitlines():
                    match = RUBRIC_LINE_RE.match(line)
                    if not match:
                        continue
                    label, _, definition = match.groups()
                    label = label.strip()
                    definition = definition.strip()
                    if not definition:
                        continue
                    key = cache_key(label, definition)
            items.setdefault(key, {"key": key, "label": label, "definition": definition})
    collected = list(items.values())
    for index, item in enumerate(collected):
        item["id"] = f"r{index:04d}"
    return collected


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


def parse_json_response(text: str) -> list[dict[str, Any]]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()
    start = cleaned.find("[")
    if start > 0:
        cleaned = cleaned[start:]
    decoder = json.JSONDecoder()
    data, _ = decoder.raw_decode(cleaned)
    if not isinstance(data, list):
        raise ValueError(f"Transform response must be a JSON list. Raw prefix: {text[:240]!r}")
    return data


def validate_item(item: dict[str, Any]) -> dict[str, str]:
    required = ("id", "expanded_en", "translated_es", "expanded_translated_es")
    missing = [field for field in required if not str(item.get(field, "")).strip()]
    if missing:
        raise ValueError(f"Missing fields in transform item: {missing}")
    return {field: str(item[field]).strip() for field in required}


def transform_batch(
    batch: list[dict[str, str]],
    args: argparse.Namespace,
    base_url: str,
    api_key: str,
) -> dict[str, dict[str, str]]:
    model_items = [
        {"id": item["id"], "label": item["label"], "definition": item["definition"]}
        for item in batch
    ]
    user_prompt = {
        "task": "Transform these moderation rubric definitions.",
        "output_schema": [
            {
                "id": "same short id from input, exactly",
                "expanded_en": "semantic-preserving expanded English definition",
                "translated_es": "Spanish translation of original definition",
                "expanded_translated_es": "Spanish translation of expanded_en",
            }
        ],
        "items": model_items,
    }
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": json.dumps(user_prompt, ensure_ascii=False)},
    ]
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
            parsed = parse_json_response(raw)
            if len(batch) == 1 and len(parsed) == 1:
                parsed[0]["id"] = batch[0]["id"]
            transformed_by_id = {item["id"]: validate_item(item) for item in parsed}
            expected = {item["id"] for item in batch}
            missing = expected - set(transformed_by_id)
            if missing:
                raise ValueError(f"Missing transformed ids: {sorted(missing)[:3]}")
            transformed = {}
            id_to_key = {item["id"]: item["key"] for item in batch}
            for item_id, value in transformed_by_id.items():
                if item_id in id_to_key:
                    value["key"] = id_to_key[item_id]
                    transformed[id_to_key[item_id]] = value
            return transformed
        except Exception as exc:
            last_error = exc
            print(f"Batch attempt {attempt + 1}/{args.retries} failed: {type(exc).__name__}: {exc}", flush=True)
            if attempt + 1 < args.retries:
                time.sleep(args.retry_sleep * (attempt + 1))
    raise RuntimeError(f"Failed to transform batch after {args.retries} attempts: {last_error}")


def main() -> None:
    load_local_env()
    args = parse_args()
    api_key = args.api_key or os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY_CONF")
    base_url = args.base_url or os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_BASE_URL_CONF") or DEFAULT_BASE_URL
    if not api_key:
        raise RuntimeError("Missing API key. Set OPENAI_API_KEY or OPENAI_API_KEY_CONF.")

    rows = json.loads(Path(args.data).read_text(encoding="utf-8"))
    items = collect_unique_rubrics(rows)
    if args.limit is not None:
        items = items[: args.limit]

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        cache = json.loads(out_path.read_text(encoding="utf-8"))
    else:
        cache = {
            "model": args.model,
            "target_language": "Spanish",
            "items": {},
        }

    cached_items = cache.setdefault("items", {})
    pending = [item for item in items if item["key"] not in cached_items]
    print(f"unique_rubrics={len(items)} cached={len(items)-len(pending)} pending={len(pending)}", flush=True)

    for start in range(0, len(pending), args.batch_size):
        batch = pending[start : start + args.batch_size]
        print(f"transforming batch {start // args.batch_size + 1} size={len(batch)}", flush=True)
        transformed = transform_batch(batch, args, base_url, api_key)
        for item in batch:
            value = transformed[item["key"]]
            value["label"] = item["label"]
            value["definition"] = item["definition"]
            cached_items[item["key"]] = value
        out_path.write_text(json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"wrote cache: {out_path}", flush=True)


if __name__ == "__main__":
    main()
