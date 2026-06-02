from __future__ import annotations

import argparse

from rewardbench_compat import (
    DPO_MODEL_CONFIG,
    load_causal_lm,
    load_tokenizer,
    official_model_name,
    pick_device,
    score_dpo_pairs,
)
from utils import compute_accuracy, load_preference_rows, write_result_bundle


DEFAULT_DATA = "/ssd1/lbh/zjx/skyjury/data/verifier_pilot_rmbench.json"
DEFAULT_REF_MODEL = "/ssd1/lbh/zjx/models/skyjury_verifier/allenai_tulu-2-dpo-7b"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate a RewardBench-compatible DPO/LM scorer on SkyJury.")
    parser.add_argument("--model", required=True, help="HF repo id or local path for the policy/DPO model.")
    parser.add_argument("--ref-model", default=DEFAULT_REF_MODEL, help="Optional reference model for log-ratio scoring.")
    parser.add_argument("--data", default=DEFAULT_DATA, help="RM-Bench-style SkyJury preference JSON.")
    parser.add_argument("--output-dir", default="/ssd1/lbh/zjx/skyjury/verifier/results")
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--max-length", type=int, default=2048)
    parser.add_argument("--max-prompt-length", type=int, default=1024)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--torch-dtype", default="auto", choices=["auto", "float16", "bfloat16", "float32"])
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--local-files-only", action="store_true", help="Do not try to reach Hugging Face Hub.")
    parser.add_argument("--device-map", default=None, help="HF device_map for CUDA runs; default is auto.")
    parser.add_argument(
        "--ref-free-type",
        default="avg",
        choices=["sum", "avg", "norm"],
        help="Reference-free or log-ratio reduction over answer tokens, matching RewardBench DPOInference options.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_preference_rows(args.data, limit=args.limit)
    device = pick_device(args.device)

    official = official_model_name(args.model)
    config = DPO_MODEL_CONFIG.get(official, DPO_MODEL_CONFIG["default"])
    trust_remote_code = args.trust_remote_code or config.trust_remote_code

    tokenizer = load_tokenizer(
        args.model,
        trust_remote_code=trust_remote_code,
        local_files_only=args.local_files_only,
        padding_side="right",
        truncation_side="left",
    )
    model = load_causal_lm(
        args.model,
        device=device,
        torch_dtype_name=args.torch_dtype,
        trust_remote_code=trust_remote_code,
        local_files_only=args.local_files_only,
        device_map=args.device_map,
    )
    ref_model = (
        load_causal_lm(
            args.ref_model,
            device=device,
            torch_dtype_name=args.torch_dtype,
            trust_remote_code=trust_remote_code,
            local_files_only=args.local_files_only,
            device_map=args.device_map,
        )
        if args.ref_model
        else None
    )
    if args.ref_model and args.model == args.ref_model:
        raise ValueError("Policy model and reference model must be different.")

    chosen_scores, rejected_scores = score_dpo_pairs(
        model=model,
        ref_model=ref_model,
        tokenizer=tokenizer,
        rows=rows,
        batch_size=args.batch_size,
        max_length=args.max_length,
        max_prompt_length=args.max_prompt_length,
        device=device,
        reduction=args.ref_free_type,
    )
    for row, chosen, rejected in zip(rows, chosen_scores, rejected_scores):
        row["score_chosen"] = chosen
        row["score_rejected"] = rejected

    metrics = compute_accuracy(rows)
    metrics.update(
        {
            "model": args.model,
            "official_model_name": official,
            "ref_model": args.ref_model,
            "method": "rewardbench_compatible_dpo_logprob"
            if args.ref_model is None
            else "rewardbench_compatible_dpo_logratio",
            "device": str(device),
            "torch_dtype": args.torch_dtype,
            "trust_remote_code": trust_remote_code,
            "ref_free_type": args.ref_free_type,
            "max_length": args.max_length,
            "max_prompt_length": args.max_prompt_length,
        }
    )
    result_path, metrics_path = write_result_bundle(
        rows=rows,
        metrics=metrics,
        output_dir=args.output_dir,
        dataset_path=args.data,
        model_name=args.model,
        method="dpo",
    )
    print(f"accuracy={metrics['accuracy']:.4f} ({metrics['correct_pairs']}/{metrics['total_pairs']})")
    print(f"predictions={result_path}")
    print(f"metrics={metrics_path}")


if __name__ == "__main__":
    main()
