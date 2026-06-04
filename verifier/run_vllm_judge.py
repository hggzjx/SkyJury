from __future__ import annotations

import argparse
import json
import random
import re
from pathlib import Path
from typing import Any

from tqdm import tqdm

from run_llm_judge import SYSTEM_PROMPT, build_user_prompt, order_plan, parse_judge_response
from utils import compute_accuracy, load_preference_rows, write_result_bundle


DEFAULT_DATA = "/ssd1/lbh/zjx/skyjury/data/skyjury_bench.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate SkyJury with a local vLLM model as judge.")
    parser.add_argument("--model-path", required=True, help="Local model path or HF repo id.")
    parser.add_argument("--model-name", default=None, help="Display/result name. Defaults to model path basename.")
    parser.add_argument("--data", default=DEFAULT_DATA)
    parser.add_argument("--output-dir", default="/ssd1/lbh/zjx/skyjury/verifier/results/vllm_judge")
    parser.add_argument("--order", choices=["normal", "swapped", "random", "bidirectional"], default="bidirectional")
    parser.add_argument("--samples", type=int, default=1)
    parser.add_argument("--seed", type=int, default=13)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=256, help="Number of judge prompts submitted per vLLM call.")
    parser.add_argument("--max-new-tokens", type=int, default=128)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--top-p", type=float, default=1.0)
    parser.add_argument("--max-model-len", type=int, default=4096)
    parser.add_argument("--tensor-parallel-size", type=int, default=1)
    parser.add_argument("--gpu-memory-utilization", type=float, default=0.90)
    parser.add_argument("--dtype", default="auto")
    parser.add_argument("--trust-remote-code", action="store_true", default=True)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def import_vllm() -> tuple[Any, Any]:
    try:
        from vllm import LLM, SamplingParams
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "vLLM is not installed in the active environment. "
            "Install it in rm_dev before running this script, e.g. `pip install vllm` "
            "with a CUDA/PyTorch-compatible version."
        ) from exc
    return LLM, SamplingParams


def build_messages(row: dict[str, Any], candidate_a: str, candidate_b: str) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_user_prompt(row["prompt"], candidate_a, candidate_b)},
    ]


def format_chat(tokenizer: Any, messages: list[dict[str, str]]) -> str:
    if hasattr(tokenizer, "apply_chat_template") and getattr(tokenizer, "chat_template", None):
        return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    return "\n\n".join(f"{msg['role'].upper()}:\n{msg['content']}" for msg in messages) + "\n\nASSISTANT:\n"


def parse_or_fallback(text: str) -> dict[str, Any]:
    try:
        return parse_judge_response(text)
    except Exception:
        match = re.search(r'"winner"\s*:\s*"([AB])"', text, flags=re.I)
        if match:
            return {"winner": match.group(1).upper(), "raw": text}
        stripped = text.strip().upper()
        if stripped in {"A", "B"}:
            return {"winner": stripped, "raw": text}
        raise


def build_tasks(rows: list[dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    tasks = []
    for row_index, row in enumerate(rows):
        rng = random.Random(args.seed + row_index)
        for pair_index, (chosen_text, rejected_text) in enumerate(zip(row["chosen"], row["rejected"])):
            for sample_index in range(args.samples):
                for swapped in order_plan(args.order, rng):
                    candidate_a = rejected_text if swapped else chosen_text
                    candidate_b = chosen_text if swapped else rejected_text
                    tasks.append(
                        {
                            "row_index": row_index,
                            "pair_index": pair_index,
                            "sample_index": sample_index,
                            "swapped": swapped,
                            "messages": build_messages(row, candidate_a, candidate_b),
                        }
                    )
    return tasks


def make_sampling_params(SamplingParams: Any, args: argparse.Namespace) -> Any:
    kwargs = {
        "temperature": args.temperature,
        "top_p": args.top_p,
        "max_tokens": args.max_new_tokens,
    }
    try:
        return SamplingParams(**kwargs, seed=args.seed)
    except TypeError:
        return SamplingParams(**kwargs)


def main() -> None:
    args = parse_args()
    rows = load_preference_rows(args.data, limit=args.limit)
    model_name = args.model_name or Path(args.model_path).name
    LLM, SamplingParams = import_vllm()

    llm = LLM(
        model=args.model_path,
        tokenizer=args.model_path,
        trust_remote_code=args.trust_remote_code,
        tensor_parallel_size=args.tensor_parallel_size,
        gpu_memory_utilization=args.gpu_memory_utilization,
        max_model_len=args.max_model_len,
        dtype=args.dtype,
        seed=args.seed,
    )
    tokenizer = llm.get_tokenizer()

    tasks = build_tasks(rows, args)
    if args.dry_run:
        print(format_chat(tokenizer, tasks[0]["messages"]))
        return

    for row in rows:
        row["score_chosen"] = [0.0 for _ in row["chosen"]]
        row["score_rejected"] = [0.0 for _ in row["rejected"]]
        row["_vote_total"] = [0.0 for _ in row["chosen"]]
        row["judge_calls"] = [[] for _ in row["chosen"]]

    sampling_params = make_sampling_params(SamplingParams, args)
    skipped = 0
    for start in tqdm(range(0, len(tasks), args.batch_size), desc="vLLM-as-judge"):
        batch = tasks[start : start + args.batch_size]
        prompts = [format_chat(tokenizer, task["messages"]) for task in batch]
        try:
            outputs = llm.generate(prompts, sampling_params, use_tqdm=False)
            texts = [output.outputs[0].text.strip() if output.outputs else "" for output in outputs]
        except Exception as exc:
            texts = [f"ERROR: {exc}" for _ in batch]

        for task, text in zip(batch, texts):
            row = rows[task["row_index"]]
            pair_index = task["pair_index"]
            try:
                parsed = parse_or_fallback(text)
                winner = parsed["winner"]
                if (winner == "A" and not task["swapped"]) or (winner == "B" and task["swapped"]):
                    row["score_chosen"][pair_index] += 1.0
                else:
                    row["score_rejected"][pair_index] += 1.0
                row["_vote_total"][pair_index] += 1.0
                row["judge_calls"][pair_index].append(
                    {
                        "sample_index": task["sample_index"],
                        "swapped": task["swapped"],
                        "winner": winner,
                        "raw": parsed["raw"],
                    }
                )
            except Exception as exc:
                skipped += 1
                row["judge_calls"][pair_index].append(
                    {
                        "sample_index": task["sample_index"],
                        "swapped": task["swapped"],
                        "winner": None,
                        "raw": text,
                        "skipped": True,
                        "error": str(exc),
                    }
                )

    skipped_rows = 0
    for row in rows:
        row_skipped = False
        for idx, total in enumerate(row.pop("_vote_total")):
            if total > 0:
                row["score_chosen"][idx] /= total
                row["score_rejected"][idx] /= total
            else:
                row["score_chosen"][idx] = 0.0
                row["score_rejected"][idx] = 0.0
                row_skipped = True
        if row_skipped:
            row["skipped"] = True
            skipped_rows += 1

    metrics = compute_accuracy(rows)
    metrics.update(
        {
            "model": model_name,
            "model_path": args.model_path,
            "method": "vllm_llm_as_judge",
            "order": args.order,
            "samples": args.samples,
            "temperature": args.temperature,
            "max_new_tokens": args.max_new_tokens,
            "batch_size": args.batch_size,
            "tensor_parallel_size": args.tensor_parallel_size,
            "gpu_memory_utilization": args.gpu_memory_utilization,
            "max_model_len": args.max_model_len,
            "skipped_calls": skipped,
            "skipped_pairs": skipped_rows,
        }
    )
    result_path, metrics_path = write_result_bundle(
        rows=rows,
        metrics=metrics,
        output_dir=args.output_dir,
        dataset_path=args.data,
        model_name=model_name,
        method="vllm_judge",
    )
    print(f"accuracy={metrics['accuracy']:.4f} ({metrics['correct_pairs']}/{metrics['total_pairs']})")
    print(f"predictions={result_path}")
    print(f"metrics={metrics_path}")


if __name__ == "__main__":
    main()
