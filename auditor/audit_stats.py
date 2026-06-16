from __future__ import annotations

import math
import random
from collections import Counter
from typing import Any

import numpy as np


OUTCOMES = ("chosen", "rejected")


def sigmoid(value: float) -> float:
    return float(1.0 / (1.0 + np.exp(-value)))


def row_margin(row: dict[str, Any]) -> float:
    chosen_scores = row.get("score_chosen", [])
    rejected_scores = row.get("score_rejected", [])
    margins: list[float] = []
    for chosen_score in chosen_scores:
        for rejected_score in rejected_scores:
            margins.append(float(chosen_score) - float(rejected_score))
    if not margins:
        raise ValueError(f"Row {row.get('id')} has no score_chosen/score_rejected values.")
    return float(np.mean(margins))


def row_preference_confidence(row: dict[str, Any]) -> float:
    chosen_scores = row.get("score_chosen", [])
    rejected_scores = row.get("score_rejected", [])
    confidences: list[float] = []
    for chosen_score in chosen_scores:
        for rejected_score in rejected_scores:
            margin = float(chosen_score) - float(rejected_score)
            confidences.append(sigmoid(margin))
    if not confidences:
        raise ValueError(f"Row {row.get('id')} has no score_chosen/score_rejected values.")
    return float(np.mean(confidences))


def paired_t_statistic(values: np.ndarray) -> float:
    if values.ndim != 1:
        raise ValueError("paired_t_statistic expects a 1D array.")
    if len(values) < 2:
        return 0.0
    std = np.std(values, ddof=1)
    if std == 0 or np.isnan(std):
        return 0.0
    return float(np.mean(values) / (std / math.sqrt(len(values))))


def cohens_d(values: np.ndarray) -> float:
    if len(values) == 0:
        return 0.0
    std = np.std(values, ddof=0)
    if std == 0 or np.isnan(std):
        return 0.0
    return float(np.mean(values) / std)


def paired_permutation_t_test(
    original_values: np.ndarray,
    perturbed_values: np.ndarray,
    permutations: int = 10000,
    seed: int = 13,
) -> dict[str, Any]:
    if original_values.shape != perturbed_values.shape:
        raise ValueError("Original and perturbed value arrays must have the same shape.")
    if original_values.ndim != 1:
        raise ValueError("Original and perturbed value arrays must be 1D.")

    delta = original_values - perturbed_values
    observed_t = paired_t_statistic(delta)
    effect = cohens_d(delta)
    if len(delta) < 2:
        return {
            "statistic": "paired_t",
            "effect_size": effect,
            "p_value": 1.0,
            "t_observed": observed_t,
            "mean_original": float(np.mean(original_values)) if len(original_values) else 0.0,
            "mean_perturbed": float(np.mean(perturbed_values)) if len(perturbed_values) else 0.0,
            "mean_delta": float(np.mean(delta)) if len(delta) else 0.0,
            "num_samples": int(len(delta)),
        }

    rng = np.random.RandomState(seed)
    signs = rng.choice(np.array([-1.0, 1.0]), size=(permutations, len(delta)))
    permuted = signs * delta
    means = np.mean(permuted, axis=1)
    stds = np.std(permuted, axis=1, ddof=1)
    t_perms = np.zeros(permutations)
    mask = stds != 0
    t_perms[mask] = means[mask] / (stds[mask] / math.sqrt(len(delta)))

    # One-sided degradation direction for preference confidence:
    # small p means the perturbation decreases confidence relative to original.
    count = int(np.sum(t_perms >= observed_t))
    p_value = float((count + 1) / (permutations + 1))
    return {
        "statistic": "paired_t",
        "effect_size": effect,
        "p_value": p_value,
        "t_observed": observed_t,
        "mean_original": float(np.mean(original_values)),
        "mean_perturbed": float(np.mean(perturbed_values)),
        "mean_delta": float(np.mean(delta)),
        "num_samples": int(len(delta)),
    }


def bh_correction(results: dict[str, dict[str, Any]], alpha: float = 0.05) -> dict[str, dict[str, Any]]:
    corrected = {key: dict(value) for key, value in results.items()}
    tests = [(key, float(value["p_value"])) for key, value in corrected.items() if "p_value" in value]
    tests.sort(key=lambda item: item[1])
    if not tests:
        return corrected

    threshold = -1.0
    m = len(tests)
    for rank, (_, p_value) in enumerate(tests, start=1):
        if p_value <= (rank / m) * alpha:
            threshold = p_value

    for key, value in corrected.items():
        p_value = float(value.get("p_value", 1.0))
        is_significant = threshold >= 0 and p_value <= threshold
        value["p_value_bh_significant"] = is_significant
        value["significance"] = significance_marker(p_value, is_significant)
        effect = float(value.get("effect_size", 0.0))
        value["robustness_risk"] = effect if is_significant else 0.0
    return corrected


def significance_marker(p_value: float, is_significant: bool) -> str:
    if not is_significant:
        return "ns"
    if p_value <= 0.001:
        return "***"
    if p_value <= 0.01:
        return "**"
    if p_value <= 0.05:
        return "*"
    return "ns"


def format_effect_marker(effect: float, marker: str) -> str:
    suffix = "" if marker == "ns" else marker
    return f"{effect:.4f}^{suffix}"


def outcome_from_call(call: dict[str, Any]) -> str:
    winner = str(call.get("winner", "")).lower()
    swapped = bool(call.get("swapped", False))
    if winner == "a":
        return "rejected" if swapped else "chosen"
    if winner == "b":
        return "chosen" if swapped else "rejected"
    raise ValueError(f"Invalid or skipped LLM judge winner: {winner!r}")


def outcomes_from_row(row: dict[str, Any]) -> list[str]:
    calls = row.get("judge_calls", [])
    outcomes: list[str] = []
    for pair_calls in calls:
        if isinstance(pair_calls, list):
            outcomes.extend(outcome_from_call(call) for call in pair_calls)
    if outcomes:
        return outcomes

    chosen_scores = row.get("score_chosen", [])
    rejected_scores = row.get("score_rejected", [])
    for chosen_score in chosen_scores:
        for rejected_score in rejected_scores:
            if float(chosen_score) > float(rejected_score):
                outcomes.append("chosen")
            elif float(chosen_score) < float(rejected_score):
                outcomes.append("rejected")
            else:
                raise ValueError(
                    f"Row {row.get('id')} has tied LLM judge scores, but current LLM-as-judge audit is binary."
                )
    if not outcomes:
        raise ValueError(f"Row {row.get('id')} has no valid binary LLM judge outcomes.")
    return outcomes


def distribution(outcomes: list[str]) -> np.ndarray:
    counts = Counter(outcomes)
    total = max(sum(counts.values()), 1)
    return np.array([counts.get(outcome, 0) / total for outcome in OUTCOMES], dtype=float)


def js_divergence(p: np.ndarray, q: np.ndarray) -> float:
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    p = p / p.sum() if p.sum() else np.ones_like(p) / len(p)
    q = q / q.sum() if q.sum() else np.ones_like(q) / len(q)
    m = 0.5 * (p + q)
    return 0.5 * kl_divergence(p, m) + 0.5 * kl_divergence(q, m)


def js_distance(p: np.ndarray, q: np.ndarray) -> float:
    return float(math.sqrt(js_divergence(p, q)))


def kl_divergence(p: np.ndarray, q: np.ndarray) -> float:
    mask = p > 0
    return float(np.sum(p[mask] * np.log2(p[mask] / q[mask])))


def llm_jsd_permutation_test(
    original_rows: list[dict[str, Any]],
    perturbed_rows: list[dict[str, Any]],
    permutations: int = 10000,
    seed: int = 13,
) -> dict[str, Any]:
    if len(original_rows) != len(perturbed_rows):
        raise ValueError("Original and perturbed LLM prediction files must contain the same number of rows.")

    pairs: list[tuple[list[str], list[str]]] = []
    observed_distances: list[float] = []
    for original_row, perturbed_row in zip(original_rows, perturbed_rows):
        original_outcomes = outcomes_from_row(original_row)
        perturbed_outcomes = outcomes_from_row(perturbed_row)
        pairs.append((original_outcomes, perturbed_outcomes))
        observed_distances.append(
            js_distance(distribution(original_outcomes), distribution(perturbed_outcomes))
        )

    observed = float(np.mean(observed_distances)) if observed_distances else 0.0
    rng = random.Random(seed)
    null_stats: list[float] = []
    for _ in range(permutations):
        distances = []
        for original_outcomes, perturbed_outcomes in pairs:
            pooled = original_outcomes + perturbed_outcomes
            n_original = len(original_outcomes)
            shuffled = pooled[:]
            rng.shuffle(shuffled)
            perm_original = shuffled[:n_original]
            perm_perturbed = shuffled[n_original:]
            distances.append(
                js_distance(distribution(perm_original), distribution(perm_perturbed))
            )
        null_stats.append(float(np.mean(distances)) if distances else 0.0)

    count = sum(stat >= observed for stat in null_stats)
    p_value = float((count + 1) / (permutations + 1))
    return {
        "statistic": "mean_per_sample_js_distance",
        "effect_size": observed,
        "p_value": p_value,
        "mean_original_chosen_rate": float(np.mean([distribution(out)[0] for out, _ in pairs])) if pairs else 0.0,
        "mean_perturbed_chosen_rate": float(np.mean([distribution(out)[0] for _, out in pairs])) if pairs else 0.0,
        "num_samples": len(pairs),
        "permutations": permutations,
    }
