from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Materialize auditor base predictions by subsetting full verifier predictions to the category50 base ids."
    )
    parser.add_argument("--base-data", required=True, help="Base auditor dataset JSON containing the target row ids.")
    parser.add_argument("--full-predictions", required=True, help="Full verifier prediction JSON.")
    parser.add_argument("--output", required=True, help="Output path for the subsetted prediction JSON.")
    return parser.parse_args()


def load_json_list(path: str | Path) -> list[dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"{path} must be a JSON list.")
    return data


def main() -> None:
    args = parse_args()
    base_rows = load_json_list(args.base_data)
    full_rows = load_json_list(args.full_predictions)

    target_ids = [row.get("id") for row in base_rows]
    if any(row_id is None for row_id in target_ids):
        raise ValueError("Base auditor dataset contains rows without an id.")

    full_by_id: dict[str, dict[str, Any]] = {}
    for row in full_rows:
        row_id = row.get("id")
        if row_id is None:
            continue
        full_by_id[row_id] = row

    subset_rows: list[dict[str, Any]] = []
    missing_ids: list[str] = []
    for row_id in target_ids:
        if row_id not in full_by_id:
            missing_ids.append(row_id)
            continue
        subset_rows.append(full_by_id[row_id])

    if missing_ids:
        raise ValueError(
            f"Full predictions are missing {len(missing_ids)} base ids, e.g. {missing_ids[:10]}"
        )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(subset_rows, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote subset predictions: {output_path}")
    print(f"num_rows={len(subset_rows)}")


if __name__ == "__main__":
    main()
