from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


def load_preference_rows(path: str | Path, limit: int | None = None) -> list[dict[str, Any]]:
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError(f"Expected a JSON list, got {type(rows).__name__}")
    if limit is not None:
        rows = rows[:limit]
    for row in rows:
        if not isinstance(row.get("chosen"), list) or not isinstance(row.get("rejected"), list):
            raise ValueError("Each row must contain list-valued `chosen` and `rejected` fields.")
        if len(row["chosen"]) != len(row["rejected"]):
            raise ValueError(f"Row {row.get('id')} has different chosen/rejected list lengths.")
    return rows


def safe_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_")


def format_policy_judgment_prompt(prompt: str, template: str = "default") -> str:
    if template == "default":
        return prompt
    if template != "strong":
        raise ValueError(f"Unsupported prompt template: {template}")

    profile = prompt.strip()
    profile = re.sub(r"^\s*User profile and behavior context:\s*", "", profile, flags=re.IGNORECASE)
    profile = re.sub(
        r"\n\s*Task:\s*Choose which candidate Bluesky Labeler is more suitable to recommend to this user\.\s*$",
        "",
        profile,
        flags=re.IGNORECASE,
    ).strip()

    return "\n".join(
        [
            "You are evaluating a candidate Bluesky labeling service for a user.",
            "",
            "User profile and behavior context:",
            profile,
            "",
            "Task:",
            "The assistant response will describe one candidate Bluesky Labeler.",
            "Score how suitable this candidate labeler is for the user's moderation needs.",
            "A better candidate should match the user's recurring cases, policy scope, rubric boundaries, and moderation intent.",
        ]
    )


def format_pair_text(tokenizer: Any, prompt: str, answer: str) -> str:
    messages = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": answer},
    ]
    if hasattr(tokenizer, "apply_chat_template") and getattr(tokenizer, "chat_template", None):
        try:
            return tokenizer.apply_chat_template(messages, tokenize=False)
        except Exception:
            pass
    return f"User:\n{prompt}\n\nAssistant:\n{answer}"


def format_prompt_prefix(tokenizer: Any, prompt: str) -> str:
    messages = [{"role": "user", "content": prompt}]
    if hasattr(tokenizer, "apply_chat_template") and getattr(tokenizer, "chat_template", None):
        try:
            return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        except Exception:
            pass
    return f"User:\n{prompt}\n\nAssistant:\n"


def compute_accuracy(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total_correct = 0
    total_pairs = 0
    subset_correct: dict[str, int] = defaultdict(int)
    subset_total: dict[str, int] = defaultdict(int)
    category_correct: dict[str, int] = defaultdict(int)
    category_total: dict[str, int] = defaultdict(int)

    for row in rows:
        subset = row.get("subset", "unknown")
        category = row.get("category", "unknown")
        score_chosen = row.get("score_chosen", [])
        score_rejected = row.get("score_rejected", [])
        if not score_chosen or not score_rejected:
            continue
        for chosen_score in score_chosen:
            for rejected_score in score_rejected:
                correct = int(chosen_score > rejected_score)
                total_correct += correct
                total_pairs += 1
                subset_correct[subset] += correct
                subset_total[subset] += 1
                category_correct[category] += correct
                category_total[category] += 1

    subset_acc = {
        subset: subset_correct[subset] / subset_total[subset]
        for subset in sorted(subset_total)
        if subset_total[subset] > 0
    }
    category_acc = {
        category: category_correct[category] / category_total[category]
        for category in sorted(category_total)
        if category_total[category] > 0
    }
    category_counts = {
        category: {
            "correct_pairs": category_correct[category],
            "total_pairs": category_total[category],
            "accuracy": category_acc[category],
        }
        for category in sorted(category_total)
        if category_total[category] > 0
    }
    return {
        "accuracy": total_correct / total_pairs if total_pairs else 0.0,
        "correct_pairs": total_correct,
        "total_pairs": total_pairs,
        "num_samples": len(rows),
        "subset_accuracy": subset_acc,
        "category_accuracy": category_acc,
        "category_metrics": category_counts,
    }


def write_result_bundle(
    rows: list[dict[str, Any]],
    metrics: dict[str, Any],
    output_dir: str | Path,
    dataset_path: str | Path,
    model_name: str,
    method: str,
) -> tuple[Path, Path]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    dataset_stem = Path(dataset_path).stem
    prefix = f"{dataset_stem}_{method}_{safe_name(model_name)}"
    result_path = output_dir / f"{prefix}_predictions.json"
    metrics_path = output_dir / f"{prefix}_metrics.json"
    result_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    metrics_path.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    return result_path, metrics_path
