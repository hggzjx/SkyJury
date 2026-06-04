from __future__ import annotations

import argparse

from rewardbench_compat import (
    format_rewardbench_pair_text,
    load_reward_model,
    load_tokenizer,
    official_model_name,
    pick_device,
    score_reward_conversations,
    score_reward_texts,
)
from utils import compute_accuracy, load_preference_rows, write_result_bundle


DEFAULT_DATA = "/ssd1/lbh/zjx/skyjury/data/skyjury_bench.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate a RewardBench-compatible reward model on SkyJury.")
    parser.add_argument("--model", required=True, help="HF repo id or local path for a reward model.")
    parser.add_argument("--data", default=DEFAULT_DATA, help="RM-Bench-style SkyJury preference JSON.")
    parser.add_argument("--output-dir", default="/ssd1/lbh/zjx/skyjury/verifier/results")
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--max-length", type=int, default=2048)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--torch-dtype", default="auto", choices=["auto", "float16", "bfloat16", "float32"])
    parser.add_argument(
        "--trust-remote-code",
        action="store_true",
        default=None,
        help="Force trust_remote_code. If omitted, use the RewardBench-compatible model config.",
    )
    parser.add_argument("--no-trust-remote-code", action="store_false", dest="trust_remote_code")
    parser.add_argument("--local-files-only", action="store_true", help="Do not try to reach Hugging Face Hub.")
    parser.add_argument("--device-map", default=None, help="HF device_map for CUDA runs; default is auto.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_preference_rows(args.data, limit=args.limit)
    device = pick_device(args.device)

    model, config, effective_trust = load_reward_model(
        args.model,
        device=device,
        torch_dtype_name=args.torch_dtype,
        trust_remote_code=args.trust_remote_code,
        local_files_only=args.local_files_only,
        device_map=args.device_map,
    )
    tokenizer = load_tokenizer(
        config.tokenizer_source or args.model,
        trust_remote_code=effective_trust,
        local_files_only=args.local_files_only,
        padding_side=config.tokenizer_padding_side,
        truncation_side=config.tokenizer_truncation_side,
    )
    if getattr(model.config, "pad_token_id", None) is None:
        model.config.pad_token_id = tokenizer.pad_token_id

    flat_texts: list[str] = []
    flat_conversations: list[list[dict[str, str]]] = []
    flat_index: list[tuple[int, str]] = []
    for row_idx, row in enumerate(rows):
        prompt = row["prompt"]
        for answer in row["chosen"]:
            if config.tokenize_chat_template:
                flat_conversations.append(
                    [{"role": "user", "content": prompt}, {"role": "assistant", "content": answer}]
                )
            else:
                flat_texts.append(format_rewardbench_pair_text(tokenizer, prompt, answer))
            flat_index.append((row_idx, "score_chosen"))
        for answer in row["rejected"]:
            if config.tokenize_chat_template:
                flat_conversations.append(
                    [{"role": "user", "content": prompt}, {"role": "assistant", "content": answer}]
                )
            else:
                flat_texts.append(format_rewardbench_pair_text(tokenizer, prompt, answer))
            flat_index.append((row_idx, "score_rejected"))

    if config.tokenize_chat_template:
        flat_scores = score_reward_conversations(
            model=model,
            tokenizer=tokenizer,
            conversations=flat_conversations,
            max_length=args.max_length,
            device=device,
            score_index=config.reward_score_index,
        )
    else:
        flat_scores = score_reward_texts(
            model=model,
            tokenizer=tokenizer,
            texts=flat_texts,
            batch_size=args.batch_size,
            max_length=args.max_length,
            device=device,
            score_index=config.reward_score_index,
            add_special_tokens=config.add_special_tokens,
        )
    for row in rows:
        row["score_chosen"] = []
        row["score_rejected"] = []
    for (row_idx, key), score in zip(flat_index, flat_scores):
        rows[row_idx][key].append(score)

    metrics = compute_accuracy(rows)
    metrics.update(
        {
            "model": args.model,
            "official_model_name": official_model_name(args.model),
            "method": "rewardbench_compatible_reward_model",
            "device": str(device),
            "torch_dtype": args.torch_dtype,
            "trust_remote_code": effective_trust,
            "model_builder": config.model_builder,
        }
    )
    result_path, metrics_path = write_result_bundle(
        rows=rows,
        metrics=metrics,
        output_dir=args.output_dir,
        dataset_path=args.data,
        model_name=args.model,
        method="rm",
    )
    print(f"accuracy={metrics['accuracy']:.4f} ({metrics['correct_pairs']}/{metrics['total_pairs']})")
    print(f"predictions={result_path}")
    print(f"metrics={metrics_path}")


if __name__ == "__main__":
    main()
