from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

from audit_stats import (
    bh_correction,
    format_effect_marker,
    paired_permutation_t_test,
    row_preference_confidence,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit SkyJury verifier predictions under rubric perturbations."
    )
    parser.add_argument(
        "--method",
        choices=["rm", "dpo", "llm_judge"],
        required=True,
        help="Verifier family. rm, dpo, and llm_judge use paired t-statistics over preference confidence.",
    )
    parser.add_argument("--original", required=True, help="Prediction JSON on the original dataset.")
    parser.add_argument(
        "--perturbed",
        action="append",
        required=True,
        metavar="TYPE=PATH",
        help="Perturbed prediction JSON. Repeat for length/language.",
    )
    parser.add_argument("--output-dir", default="/ssd1/lbh/zjx/skyjury/auditor/results")
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--permutations", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=13)
    parser.add_argument("--report-name", default=None)
    parser.add_argument(
        "--allow-subset",
        action="store_true",
        help="Allow perturbed predictions to contain only a verifier-success subset of the original predictions.",
    )
    return parser.parse_args()


def load_rows(path: str | Path) -> list[dict[str, Any]]:
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError(f"{path} must be a JSON list.")
    return rows


def parse_perturbed_specs(specs: list[str]) -> dict[str, Path]:
    parsed: dict[str, Path] = {}
    for spec in specs:
        if "=" not in spec:
            raise ValueError(f"Expected TYPE=PATH for --perturbed, got: {spec}")
        name, path = spec.split("=", 1)
        name = name.strip()
        if not name:
            raise ValueError(f"Empty perturbation type in: {spec}")
        parsed[name] = Path(path)
    return parsed


def align_rows(
    original_rows: list[dict[str, Any]],
    perturbed_rows: list[dict[str, Any]],
    allow_subset: bool = False,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    original_by_id = {row.get("id"): row for row in original_rows}
    perturbed_by_id = {row.get("id"): row for row in perturbed_rows}
    aligned_original = []
    aligned_perturbed = []
    missing = []
    extra = []
    if allow_subset:
        row_ids = [row.get("id") for row in perturbed_rows]
        for row_id in row_ids:
            if row_id not in original_by_id:
                extra.append(row_id)
                continue
            aligned_original.append(original_by_id[row_id])
            aligned_perturbed.append(perturbed_by_id[row_id])
        if extra:
            raise ValueError(f"Perturbed predictions contain ids missing from original, e.g. {extra[:5]}")
        return aligned_original, aligned_perturbed

    for row_id, row in original_by_id.items():
        if row_id not in perturbed_by_id:
            missing.append(row_id)
            continue
        aligned_original.append(row)
        aligned_perturbed.append(perturbed_by_id[row_id])
    if missing:
        raise ValueError(
            f"Perturbed predictions are missing {len(missing)} row ids, e.g. {missing[:5]}. "
            "Use --allow-subset when auditing only verifier-success cases."
        )
    for row_id in perturbed_by_id:
        if row_id not in original_by_id:
            extra.append(row_id)
    if extra:
        raise ValueError(f"Perturbed predictions contain ids missing from original, e.g. {extra[:5]}")
    return aligned_original, aligned_perturbed


def audit_scalar_scores(
    original_rows: list[dict[str, Any]],
    perturbed_rows: list[dict[str, Any]],
    permutations: int,
    seed: int,
) -> dict[str, Any]:
    original_confidence = np.array([row_preference_confidence(row) for row in original_rows], dtype=float)
    perturbed_confidence = np.array([row_preference_confidence(row) for row in perturbed_rows], dtype=float)
    result = paired_permutation_t_test(
        original_confidence,
        perturbed_confidence,
        permutations=permutations,
        seed=seed,
    )
    result["metric"] = "preference_confidence=sigmoid(chosen_score - rejected_score)"
    result["direction"] = "right-tailed test on original_confidence - perturbed_confidence"
    result["permutations"] = permutations
    return result


def has_valid_scalar_scores(row: dict[str, Any]) -> bool:
    chosen_scores = row.get("score_chosen", [])
    rejected_scores = row.get("score_rejected", [])
    return bool(chosen_scores) and bool(rejected_scores)


def audit_one(
    method: str,
    original_rows: list[dict[str, Any]],
    perturbed_rows: list[dict[str, Any]],
    permutations: int,
    seed: int,
    allow_subset: bool,
) -> dict[str, Any]:
    aligned_original, aligned_perturbed = align_rows(original_rows, perturbed_rows, allow_subset=allow_subset)
    valid_pairs = [
        (original_row, perturbed_row)
        for original_row, perturbed_row in zip(aligned_original, aligned_perturbed)
        if has_valid_scalar_scores(original_row) and has_valid_scalar_scores(perturbed_row)
    ]
    dropped_row_ids = [
        original_row.get("id")
        for original_row, perturbed_row in zip(aligned_original, aligned_perturbed)
        if not (has_valid_scalar_scores(original_row) and has_valid_scalar_scores(perturbed_row))
    ]
    if not valid_pairs:
        raise ValueError("No valid aligned rows remain after filtering empty score pairs.")

    filtered_original = [original_row for original_row, _ in valid_pairs]
    filtered_perturbed = [perturbed_row for _, perturbed_row in valid_pairs]
    result = audit_scalar_scores(filtered_original, filtered_perturbed, permutations, seed)
    result["audited_num_samples"] = len(aligned_original)
    result["audited_row_ids"] = [row.get("id") for row in filtered_original]
    result["audited_num_samples_raw"] = len(aligned_original)
    result["audited_num_samples"] = len(filtered_original)
    result["dropped_invalid_score_rows"] = len(dropped_row_ids)
    result["dropped_invalid_score_row_ids"] = dropped_row_ids
    return result


def categories_in_rows(rows: list[dict[str, Any]]) -> list[str]:
    return sorted({row.get("category", "unknown") for row in rows})


def filter_rows_by_category(rows: list[dict[str, Any]], category: str) -> list[dict[str, Any]]:
    return [row for row in rows if row.get("category", "unknown") == category]


def result_key(scope: str, perturbation: str) -> str:
    return f"{scope}::{perturbation}"


def split_result_key(key: str) -> tuple[str, str]:
    if "::" not in key:
        return "overall", key
    scope, perturbation = key.split("::", 1)
    return scope, perturbation


def write_markdown_report(
    output_path: Path,
    method: str,
    original_path: Path,
    corrected: dict[str, dict[str, Any]],
    allow_subset: bool,
) -> None:
    lines = [
        "# SkyJury Auditor Robustness Risk Report",
        "",
        f"- method: `{method}`",
        f"- original_predictions: `{original_path}`",
        f"- audited_cases: `{'verifier-success subset' if allow_subset else 'all original cases'}`",
        "- multiple-testing control: Benjamini-Hochberg (BH)",
        "",
        "## Overall",
        "",
        "| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |",
        "| --- | ---: | --- | ---: | ---: | ---: | --- |",
    ]
    category_items: dict[str, list[tuple[str, dict[str, Any]]]] = {}
    for key, result in corrected.items():
        scope, perturbation = split_result_key(key)
        if scope != "overall":
            category = scope[len("category:") :] if scope.startswith("category:") else scope
            category_items.setdefault(category, []).append((perturbation, result))
            continue
        marker = result.get("significance", "ns")
        effect = float(result.get("effect_size", 0.0))
        p_value = float(result.get("p_value", 1.0))
        risk = float(result.get("robustness_risk", 0.0))
        if result.get("statistic") == "mean_per_sample_js_distance":
            summary = (
                f"chosen_rate {result.get('mean_original_chosen_rate', 0.0):.3f}"
                f" -> {result.get('mean_perturbed_chosen_rate', 0.0):.3f}"
            )
        else:
            summary = (
                f"confidence {result.get('mean_original', 0.0):.4f}"
                f" -> {result.get('mean_perturbed', 0.0):.4f}"
            )
        lines.append(
            f"| {perturbation} | {result.get('audited_num_samples', result.get('num_samples', ''))} | "
            f"{result.get('statistic')} | "
            f"{format_effect_marker(effect, marker)} | {p_value:.6f} | {risk:.4f} | {summary} |"
        )
    for category in sorted(category_items):
        lines.extend(
            [
                "",
                f"## Category: `{category}`",
                "",
                "| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |",
                "| --- | ---: | --- | ---: | ---: | ---: | --- |",
            ]
        )
        for perturbation, result in sorted(category_items[category]):
            marker = result.get("significance", "ns")
            effect = float(result.get("effect_size", 0.0))
            p_value = float(result.get("p_value", 1.0))
            risk = float(result.get("robustness_risk", 0.0))
            if result.get("statistic") == "mean_per_sample_js_distance":
                summary = (
                    f"chosen_rate {result.get('mean_original_chosen_rate', 0.0):.3f}"
                    f" -> {result.get('mean_perturbed_chosen_rate', 0.0):.3f}"
                )
            else:
                summary = (
                    f"confidence {result.get('mean_original', 0.0):.4f}"
                    f" -> {result.get('mean_perturbed', 0.0):.4f}"
                )
            lines.append(
                f"| {perturbation} | {result.get('audited_num_samples', result.get('num_samples', ''))} | "
                f"{result.get('statistic')} | "
                f"{format_effect_marker(effect, marker)} | {p_value:.6f} | {risk:.4f} | {summary} |"
            )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    original_path = Path(args.original)
    original_rows = load_rows(original_path)
    perturbed_specs = parse_perturbed_specs(args.perturbed)

    raw_results = {}
    categories = categories_in_rows(original_rows)
    for index, (perturbation, path) in enumerate(perturbed_specs.items()):
        perturbed_rows = load_rows(path)
        raw_results[result_key("overall", perturbation)] = audit_one(
            method=args.method,
            original_rows=original_rows,
            perturbed_rows=perturbed_rows,
            permutations=args.permutations,
            seed=args.seed + index,
            allow_subset=args.allow_subset,
        )
        for category_index, category in enumerate(categories):
            original_category_rows = filter_rows_by_category(original_rows, category)
            perturbed_category_rows = filter_rows_by_category(perturbed_rows, category)
            if not perturbed_category_rows:
                continue
            raw_results[result_key(f"category:{category}", perturbation)] = audit_one(
                method=args.method,
                original_rows=original_category_rows,
                perturbed_rows=perturbed_category_rows,
                permutations=args.permutations,
                seed=args.seed + index + 1000 * (category_index + 1),
                allow_subset=args.allow_subset,
            )

    corrected = bh_correction(raw_results, alpha=args.alpha)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = args.report_name or f"{args.method}_rubric_robustness"
    json_path = output_dir / f"{stem}.json"
    md_path = output_dir / f"{stem}.md"
    json_path.write_text(json.dumps(corrected, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown_report(md_path, args.method, original_path, corrected, allow_subset=args.allow_subset)
    print(f"wrote json: {json_path}")
    print(f"wrote report: {md_path}")


if __name__ == "__main__":
    main()
