from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_DATA = "/ssd1/lbh/zjx/skyjury/data/verifier_pilot_rmbench.json"
DEFAULT_OUTPUT_DIR = "/ssd1/lbh/zjx/skyjury/data/auditor"

PERTURBATION_TYPES = ("length", "language", "length_language")


RUBRIC_LINE_RE = re.compile(r"^(\s*-\s+)([^:\n]+?)(:\s*)(.*)$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build rubric-only perturbation datasets for SkyJury auditor."
    )
    parser.add_argument("--data", default=DEFAULT_DATA, help="Original SkyJury preference JSON.")
    parser.add_argument(
        "--verifier-predictions",
        default=None,
        help="Optional verifier prediction JSON. When set with --success-only, only verifier-correct cases enter auditor data.",
    )
    parser.add_argument(
        "--success-only",
        action="store_true",
        help="Keep only rows where every chosen/rejected score pair is correctly ordered.",
    )
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--prefix",
        default=None,
        help="Output filename prefix. Defaults to the input dataset stem.",
    )
    return parser.parse_args()


def load_rows(path: str | Path) -> list[dict[str, Any]]:
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError("Input dataset must be a JSON list.")
    return rows


def canonical_sha256(rows: list[dict[str, Any]]) -> str:
    payload = json.dumps(rows, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def is_successful_verifier_row(row: dict[str, Any]) -> bool:
    chosen_scores = row.get("score_chosen", [])
    rejected_scores = row.get("score_rejected", [])
    if not chosen_scores or not rejected_scores:
        return False
    return all(float(chosen) > float(rejected) for chosen in chosen_scores for rejected in rejected_scores)


def strip_prediction_fields(row: dict[str, Any]) -> dict[str, Any]:
    stripped = copy.deepcopy(row)
    for key in ("score_chosen", "score_rejected", "judge_calls"):
        stripped.pop(key, None)
    return stripped


def filter_to_successful_cases(
    data_rows: list[dict[str, Any]],
    prediction_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    data_by_id = {row.get("id"): row for row in data_rows}
    success_ids = [row.get("id") for row in prediction_rows if is_successful_verifier_row(row)]
    missing = [row_id for row_id in success_ids if row_id not in data_by_id]
    if missing:
        raise ValueError(f"Verifier predictions contain ids missing from data, e.g. {missing[:5]}")
    return [strip_prediction_fields(data_by_id[row_id]) for row_id in success_ids]


def split_rubrics(candidate: str) -> tuple[str, str]:
    marker = "Rubrics:"
    if marker not in candidate:
        return candidate, ""
    before, after = candidate.split(marker, 1)
    return before + marker, after


def perturb_definition(definition: str, perturbation_type: str) -> str:
    definition = definition.strip()
    if perturbation_type == "length":
        return (
            f"{definition} Operational restatement: this label should be applied only when "
            f"the same condition described above is present; the restatement does not add, "
            f"remove, broaden, or narrow any category beyond the original rubric."
        )
    if perturbation_type == "language":
        return (
            f"中文等价提示：该标签仍然只表示下列英文定义中的同一含义，不扩展也不收窄适用范围。"
            f"Original definition: {definition}"
        )
    if perturbation_type == "length_language":
        return (
            f"中文等价提示：该标签仅在原定义所描述的同一条件出现时适用；这里的中文说明只是换一种语言表达，"
            f"不引入新的审核类别，也不改变边界。Original definition: {definition} "
            f"Operational restatement: apply the label only for the same behavior, account state, "
            f"or content pattern specified in the original definition."
        )
    raise ValueError(f"Unknown perturbation type: {perturbation_type}")


def perturb_rubric_line(line: str, perturbation_type: str) -> str:
    match = RUBRIC_LINE_RE.match(line)
    if not match:
        return line
    prefix, label_name, sep, definition = match.groups()
    if not definition.strip():
        return line
    return f"{prefix}{label_name}{sep}{perturb_definition(definition, perturbation_type)}"


def perturb_candidate(candidate: str, perturbation_type: str) -> str:
    before, rubric_block = split_rubrics(candidate)
    if not rubric_block:
        return candidate
    perturbed_lines = [
        perturb_rubric_line(line, perturbation_type)
        for line in rubric_block.splitlines()
    ]
    return before + "\n".join(perturbed_lines)


def perturb_answer_list(answers: list[str], perturbation_type: str) -> list[str]:
    return [perturb_candidate(answer, perturbation_type) for answer in answers]


def build_variant(rows: list[dict[str, Any]], perturbation_type: str) -> list[dict[str, Any]]:
    variant = copy.deepcopy(rows)
    for row in variant:
        row["chosen"] = perturb_answer_list(row.get("chosen", []), perturbation_type)
        row["rejected"] = perturb_answer_list(row.get("rejected", []), perturbation_type)
    return variant


def count_changed_candidates(original: list[dict[str, Any]], variant: list[dict[str, Any]]) -> int:
    changed = 0
    for row_o, row_v in zip(original, variant):
        for key in ("chosen", "rejected"):
            for item_o, item_v in zip(row_o.get(key, []), row_v.get(key, [])):
                changed += int(item_o != item_v)
    return changed


def main() -> None:
    args = parse_args()
    data_path = Path(args.data)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = load_rows(data_path)
    source_prediction_path = None
    total_prediction_rows = None
    if args.success_only:
        if not args.verifier_predictions:
            raise ValueError("--success-only requires --verifier-predictions.")
        source_prediction_path = Path(args.verifier_predictions)
        prediction_rows = load_rows(source_prediction_path)
        total_prediction_rows = len(prediction_rows)
        rows = filter_to_successful_cases(rows, prediction_rows)
    prefix = args.prefix or data_path.stem
    base_path = output_dir / f"{prefix}_base.json"
    base_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")

    manifest: dict[str, Any] = {
        "source_data": str(data_path),
        "source_data_sha256": canonical_sha256(rows),
        "base_path": str(base_path),
        "source_verifier_predictions": str(source_prediction_path) if source_prediction_path else None,
        "num_rows": len(rows),
        "total_prediction_rows": total_prediction_rows,
        "success_only": args.success_only,
        "perturbation_scope": "rubrics_only",
        "semantic_constraint": "Perturbations preserve the original rubric meaning.",
        "variants": {},
    }

    for perturbation_type in PERTURBATION_TYPES:
        variant = build_variant(rows, perturbation_type)
        out_path = output_dir / f"{prefix}_rubric_{perturbation_type}.json"
        out_path.write_text(json.dumps(variant, indent=2, ensure_ascii=False), encoding="utf-8")
        manifest["variants"][perturbation_type] = {
            "path": str(out_path),
            "changed_candidates": count_changed_candidates(rows, variant),
        }

    manifest_path = output_dir / f"{prefix}_rubric_perturbation_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote manifest: {manifest_path}")
    print(f"base: {base_path}")
    for name, meta in manifest["variants"].items():
        print(f"{name}: {meta['path']} changed_candidates={meta['changed_candidates']}")


if __name__ == "__main__":
    main()
