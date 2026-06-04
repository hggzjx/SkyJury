from __future__ import annotations

import argparse
import json
import random
import re
from pathlib import Path
from typing import Any

import torch
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

from run_llm_judge import SYSTEM_PROMPT, build_user_prompt, order_plan, parse_judge_response
from utils import compute_accuracy, load_preference_rows, write_result_bundle


DEFAULT_DATA = "/ssd1/lbh/zjx/skyjury/data/skyjury_bench.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate SkyJury with a local HF causal LM as judge.")
    parser.add_argument("--model-path", required=True, help="Local model path or HF repo id.")
    parser.add_argument("--model-name", default=None, help="Display/result name. Defaults to model path basename.")
    parser.add_argument("--data", default=DEFAULT_DATA)
    parser.add_argument("--output-dir", default="/ssd1/lbh/zjx/skyjury/verifier/results/local_llm_judge")
    parser.add_argument("--order", choices=["normal", "swapped", "random", "bidirectional"], default="bidirectional")
    parser.add_argument("--samples", type=int, default=1)
    parser.add_argument("--seed", type=int, default=13)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--max-new-tokens", type=int, default=128)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--top-p", type=float, default=1.0)
    parser.add_argument("--max-input-length", type=int, default=4096)
    parser.add_argument("--device-map", default="auto")
    parser.add_argument("--torch-dtype", default="auto", choices=["auto", "float16", "bfloat16", "float32"])
    parser.add_argument("--trust-remote-code", action="store_true", default=True)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def dtype_from_name(name: str) -> str | torch.dtype:
    if name == "auto":
        return "auto"
    return {
        "float16": torch.float16,
        "bfloat16": torch.bfloat16,
        "float32": torch.float32,
    }[name]


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


def generate_batch(
    model: Any,
    tokenizer: Any,
    prompts: list[str],
    args: argparse.Namespace,
) -> list[str]:
    encoded = tokenizer(
        prompts,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=args.max_input_length,
    )
    input_device = next(model.parameters()).device
    encoded = {key: value.to(input_device) for key, value in encoded.items()}
    input_lengths = encoded["attention_mask"].sum(dim=1).tolist()
    do_sample = args.temperature > 0
    with torch.inference_mode():
        generation_kwargs = {
            "max_new_tokens": args.max_new_tokens,
            "do_sample": do_sample,
            "pad_token_id": tokenizer.eos_token_id,
        }
        if do_sample:
            generation_kwargs["temperature"] = args.temperature
            generation_kwargs["top_p"] = args.top_p
        output_ids = model.generate(**encoded, **generation_kwargs)
    texts = []
    for ids, input_length in zip(output_ids, input_lengths):
        generated = ids[int(input_length) :]
        texts.append(tokenizer.decode(generated, skip_special_tokens=True).strip())
    return texts


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


def main() -> None:
    args = parse_args()
    rows = load_preference_rows(args.data, limit=args.limit)
    model_name = args.model_name or Path(args.model_path).name

    tokenizer = AutoTokenizer.from_pretrained(args.model_path, trust_remote_code=args.trust_remote_code)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"
    model = AutoModelForCausalLM.from_pretrained(
        args.model_path,
        device_map=args.device_map,
        torch_dtype=dtype_from_name(args.torch_dtype),
        trust_remote_code=args.trust_remote_code,
    )
    model.eval()

    tasks = build_tasks(rows, args)
    if args.dry_run:
        print(format_chat(tokenizer, tasks[0]["messages"]))
        return

    for row in rows:
        row["score_chosen"] = [0.0 for _ in row["chosen"]]
        row["score_rejected"] = [0.0 for _ in row["rejected"]]
        row["_vote_total"] = [0.0 for _ in row["chosen"]]
        row["judge_calls"] = [[] for _ in row["chosen"]]

    skipped = 0
    for start in tqdm(range(0, len(tasks), args.batch_size), desc="Local LLM-as-judge"):
        batch = tasks[start : start + args.batch_size]
        prompts = [format_chat(tokenizer, task["messages"]) for task in batch]
        try:
            outputs = generate_batch(model, tokenizer, prompts, args)
        except Exception as exc:
            outputs = [f"ERROR: {exc}" for _ in batch]

        for task, output in zip(batch, outputs):
            row = rows[task["row_index"]]
            pair_index = task["pair_index"]
            try:
                parsed = parse_or_fallback(output)
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
                        "raw": output,
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
            "method": "local_llm_as_judge",
            "order": args.order,
            "samples": args.samples,
            "temperature": args.temperature,
            "max_new_tokens": args.max_new_tokens,
            "batch_size": args.batch_size,
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
        method="local_llm_judge",
    )
    print(f"accuracy={metrics['accuracy']:.4f} ({metrics['correct_pairs']}/{metrics['total_pairs']})")
    print(f"predictions={result_path}")
    print(f"metrics={metrics_path}")


if __name__ == "__main__":
    main()
