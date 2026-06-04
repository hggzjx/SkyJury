from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Any


DEFAULT_DATA_DIR = "/ssd1/lbh/zjx/skyjury/data/auditor"
DEFAULT_OUTPUT_DIR = "/ssd1/lbh/zjx/skyjury/data/auditor/category50"
DEFAULT_PREFIX = "skyjury_bench"
PERTURBATIONS = ("length", "language", "length_language")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a category-balanced SkyJury auditor subset.")
    parser.add_argument("--data-dir", default=DEFAULT_DATA_DIR)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--prefix", default=DEFAULT_PREFIX)
    parser.add_argument("--per-category", type=int, default=50)
    parser.add_argument("--seed", type=int, default=13)
    return parser.parse_args()


def load_json(path: Path) -> list[dict[str, Any]]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError(f"{path} must be a JSON list.")
    return rows


def write_json(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")


def sample_ids_by_category(
    rows: list[dict[str, Any]],
    per_category: int,
    seed: int,
) -> tuple[list[str], dict[str, int]]:
    by_category: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        category = str(row.get("category", "unknown"))
        by_category[category].append(str(row["id"]))

    rng = random.Random(seed)
    selected: list[str] = []
    counts: dict[str, int] = {}
    for category in sorted(by_category):
        row_ids = sorted(by_category[category])
        if len(row_ids) > per_category:
            row_ids = sorted(rng.sample(row_ids, per_category))
        counts[category] = len(row_ids)
        selected.extend(row_ids)
    return selected, counts


def subset_rows(rows: list[dict[str, Any]], selected_ids: set[str]) -> list[dict[str, Any]]:
    return [row for row in rows if str(row.get("id")) in selected_ids]


def main() -> None:
    args = parse_args()
    data_dir = Path(args.data_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    base_path = data_dir / f"{args.prefix}_base.json"
    base_rows = load_json(base_path)
    selected_order, counts = sample_ids_by_category(base_rows, args.per_category, args.seed)
    selected_ids = set(selected_order)

    active_files = {
        "base": base_path,
        "rubric_length": data_dir / f"{args.prefix}_rubric_length.json",
        "rubric_language": data_dir / f"{args.prefix}_rubric_language.json",
        "rubric_length_language": data_dir / f"{args.prefix}_rubric_length_language.json",
    }
    outputs = {}
    for name, path in active_files.items():
        rows = load_json(path)
        subset = subset_rows(rows, selected_ids)
        if len(subset) != len(selected_ids):
            raise ValueError(f"{path} only yielded {len(subset)} rows for {len(selected_ids)} selected ids.")
        out_path = output_dir / f"{args.prefix}_{name}.json"
        write_json(out_path, subset)
        outputs[name] = str(out_path)

    manifest = {
        "source_data_dir": str(data_dir),
        "prefix": args.prefix,
        "sampling_unit": "category",
        "per_category": args.per_category,
        "seed": args.seed,
        "num_rows": len(selected_ids),
        "category_counts": counts,
        "selected_ids": selected_order,
        "outputs": outputs,
    }
    manifest_path = output_dir / f"{args.prefix}_category50_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote category-balanced subset: {output_dir}")
    print(f"num_rows={len(selected_ids)} category_counts={counts}")


if __name__ == "__main__":
    main()
