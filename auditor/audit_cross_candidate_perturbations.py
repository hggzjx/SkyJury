from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

from audit_predictions import align_rows, categories_in_rows, filter_rows_by_category, has_valid_scalar_scores
from audit_stats import bh_correction, format_effect_marker, paired_permutation_t_test, sigmoid


VARIANTS = ("both", "chosen_only", "rejected_only")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit cross-candidate rubric perturbations from existing SkyJury prediction scores."
    )
    parser.add_argument("--method", choices=["rm", "dpo", "llm_judge"], required=True)
    parser.add_argument("--original", required=True)
    parser.add_argument(
        "--perturbed",
        action="append",
        required=True,
        metavar="TYPE=PATH",
        help="Perturbed prediction JSON. Use length=PATH and language=PATH.",
    )
    parser.add_argument("--output-dir", default="/ssd1/lbh/zjx/skyjury/auditor/results")
    parser.add_argument("--report-name", default="cross_candidate_rubric_robustness")
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--permutations", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=13)
    parser.add_argument("--allow-subset", action="store_true")
    return parser.parse_args()


def load_rows(path: str | Path) -> list[dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"{path} must be a JSON list.")
    return data


def parse_specs(specs: list[str]) -> dict[str, Path]:
    parsed: dict[str, Path] = {}
    for spec in specs:
        if "=" not in spec:
            raise ValueError(f"Expected TYPE=PATH, got: {spec}")
        name, path = spec.split("=", 1)
        name = name.strip()
        if name not in {"length", "language"}:
            raise ValueError(f"Cross-candidate audit only supports length/language, got: {name}")
        parsed[name] = Path(path)
    return parsed


def preference_confidence_from_scores(chosen_scores: list[float], rejected_scores: list[float]) -> float:
    values: list[float] = []
    for chosen_score in chosen_scores:
        for rejected_score in rejected_scores:
            values.append(sigmoid(float(chosen_score) - float(rejected_score)))
    if not values:
        raise ValueError("Cannot compute preference confidence from empty scores.")
    return float(np.mean(values))


def row_confidence(original: dict[str, Any], perturbed: dict[str, Any], variant: str) -> float:
    original_chosen = original.get("score_chosen", [])
    original_rejected = original.get("score_rejected", [])
    perturbed_chosen = perturbed.get("score_chosen", [])
    perturbed_rejected = perturbed.get("score_rejected", [])

    if variant == "both":
        return preference_confidence_from_scores(perturbed_chosen, perturbed_rejected)
    if variant == "chosen_only":
        return preference_confidence_from_scores(perturbed_chosen, original_rejected)
    if variant == "rejected_only":
        return preference_confidence_from_scores(original_chosen, perturbed_rejected)
    raise ValueError(f"Unknown variant: {variant}")


def result_key(scope: str, perturbation: str, variant: str) -> str:
    return f"{scope}::{perturbation}::{variant}"


def split_key(key: str) -> tuple[str, str, str]:
    parts = key.split("::")
    if len(parts) == 3:
        return parts[0], parts[1], parts[2]
    raise ValueError(f"Unexpected result key: {key}")


def audit_one(
    original_rows: list[dict[str, Any]],
    perturbed_rows: list[dict[str, Any]],
    perturbation: str,
    variant: str,
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
    dropped_ids = [
        original_row.get("id")
        for original_row, perturbed_row in zip(aligned_original, aligned_perturbed)
        if not (has_valid_scalar_scores(original_row) and has_valid_scalar_scores(perturbed_row))
    ]
    if not valid_pairs:
        raise ValueError("No valid aligned rows remain after filtering empty score pairs.")

    original_conf = np.array(
        [
            preference_confidence_from_scores(
                original_row.get("score_chosen", []),
                original_row.get("score_rejected", []),
            )
            for original_row, _ in valid_pairs
        ],
        dtype=float,
    )
    perturbed_conf = np.array(
        [row_confidence(original_row, perturbed_row, variant) for original_row, perturbed_row in valid_pairs],
        dtype=float,
    )
    result = paired_permutation_t_test(
        original_conf,
        perturbed_conf,
        permutations=permutations,
        seed=seed,
    )
    result.update(
        {
            "metric": "preference_confidence=sigmoid(chosen_score - rejected_score)",
            "direction": "right-tailed test on original_confidence - perturbed_confidence",
            "perturbation": perturbation,
            "variant": variant,
            "audited_num_samples_raw": len(aligned_original),
            "audited_num_samples": len(valid_pairs),
            "audited_row_ids": [original_row.get("id") for original_row, _ in valid_pairs],
            "dropped_invalid_score_rows": len(dropped_ids),
            "dropped_invalid_score_row_ids": dropped_ids,
            "permutations": permutations,
        }
    )
    return result


def write_markdown(path: Path, method: str, corrected: dict[str, dict[str, Any]]) -> None:
    lines = [
        "# SkyJury Cross-Candidate Auditor Report",
        "",
        f"- method: `{method}`",
        "- variants: `both`, `chosen_only`, `rejected_only`",
        "- multiple-testing control: Benjamini-Hochberg (BH)",
        "",
        "## Overall",
        "",
        "| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    categories: dict[str, list[tuple[str, dict[str, Any]]]] = {}
    for key, result in corrected.items():
        scope, perturbation, variant = split_key(key)
        if scope != "overall":
            category = scope[len("category:") :] if scope.startswith("category:") else scope
            categories.setdefault(category, []).append((key, result))
            continue
        marker = result.get("significance", "ns")
        effect = float(result.get("effect_size", 0.0))
        p_value = float(result.get("p_value", 1.0))
        risk = float(result.get("robustness_risk", 0.0))
        summary = f"{result.get('mean_original', 0.0):.4f} -> {result.get('mean_perturbed', 0.0):.4f}"
        lines.append(
            f"| {perturbation} | {variant} | {result.get('audited_num_samples', '')} | "
            f"{format_effect_marker(effect, marker)} | {p_value:.6f} | {risk:.4f} | {summary} |"
        )

    for category in sorted(categories):
        lines.extend(
            [
                "",
                f"## Category: `{category}`",
                "",
                "| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |",
                "| --- | --- | ---: | ---: | ---: | ---: | --- |",
            ]
        )
        for key, result in sorted(categories[category]):
            _, perturbation, variant = split_key(key)
            marker = result.get("significance", "ns")
            effect = float(result.get("effect_size", 0.0))
            p_value = float(result.get("p_value", 1.0))
            risk = float(result.get("robustness_risk", 0.0))
            summary = f"{result.get('mean_original', 0.0):.4f} -> {result.get('mean_perturbed', 0.0):.4f}"
            lines.append(
                f"| {perturbation} | {variant} | {result.get('audited_num_samples', '')} | "
                f"{format_effect_marker(effect, marker)} | {p_value:.6f} | {risk:.4f} | {summary} |"
            )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    original_rows = load_rows(args.original)
    perturbed_specs = parse_specs(args.perturbed)

    raw_results: dict[str, dict[str, Any]] = {}
    categories = categories_in_rows(original_rows)
    test_index = 0
    for perturbation, path in sorted(perturbed_specs.items()):
        perturbed_rows = load_rows(path)
        for variant in VARIANTS:
            raw_results[result_key("overall", perturbation, variant)] = audit_one(
                original_rows=original_rows,
                perturbed_rows=perturbed_rows,
                perturbation=perturbation,
                variant=variant,
                permutations=args.permutations,
                seed=args.seed + test_index,
                allow_subset=args.allow_subset,
            )
            test_index += 1
            for category_index, category in enumerate(categories):
                original_category = filter_rows_by_category(original_rows, category)
                perturbed_category = filter_rows_by_category(perturbed_rows, category)
                if not perturbed_category:
                    continue
                raw_results[result_key(f"category:{category}", perturbation, variant)] = audit_one(
                    original_rows=original_category,
                    perturbed_rows=perturbed_category,
                    perturbation=perturbation,
                    variant=variant,
                    permutations=args.permutations,
                    seed=args.seed + test_index + 1000 * (category_index + 1),
                    allow_subset=args.allow_subset,
                )
            test_index += 1

    corrected = bh_correction(raw_results, alpha=args.alpha)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{args.report_name}.json"
    md_path = output_dir / f"{args.report_name}.md"
    json_path.write_text(json.dumps(corrected, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(md_path, args.method, corrected)
    print(f"wrote json: {json_path}")
    print(f"wrote report: {md_path}")


if __name__ == "__main__":
    main()
