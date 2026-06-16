from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from utils import compute_accuracy, load_preference_rows, write_result_bundle


DEFAULT_DATA = "/ssd1/lbh/zjx/skyjury/data/skyjury_bench.json"
DEFAULT_E5_MODEL = "/ssd1/lbh/zjx/models/embeddings/intfloat_e5-base-v2"
DEFAULT_SBERT_MODEL = "/ssd1/lbh/zjx/mmm/models/paraphrase-multilingual-MiniLM-L12-v2"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate similarity-based matching models on SkyJury."
    )
    parser.add_argument(
        "--method",
        choices=["tfidf", "bm25", "sbert", "e5", "reranker"],
        required=True,
        help="Similarity-style scorer used as s_theta(user, labeler). Embeddings compute similarity; rerankers output pair scores directly.",
    )
    parser.add_argument("--data", default=DEFAULT_DATA, help="SkyJury preference JSON.")
    parser.add_argument("--output-dir", default="/ssd1/lbh/zjx/skyjury/verifier/results/similarity_models")
    parser.add_argument(
        "--fit-data",
        action="append",
        default=[],
        help=(
            "Optional JSON file used to fit lexical statistics for TF-IDF/BM25. "
            "Repeat to fit on a fixed corpus shared by original and perturbation runs."
        ),
    )
    parser.add_argument("--model-path", default=None, help="Local dense embedding model path for sbert/e5.")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--reranker-batch-size", type=int, default=None)
    parser.add_argument("--max-length", type=int, default=512)
    parser.add_argument("--reranker-max-length", type=int, default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument(
        "--pooling",
        default="mean",
        choices=["mean", "cls", "last_token"],
        help="Pooling strategy for dense transformers embeddings.",
    )
    parser.add_argument(
        "--query-instruction",
        default=None,
        help="Optional instruction prepended to user-profile queries as 'Instruct: ...\\nQuery: ...'.",
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=10,
        help="Print dense embedding progress every N batches. Use 0 to disable.",
    )
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument(
        "--cuda-devices",
        default=None,
        help="Optional CUDA_VISIBLE_DEVICES value, e.g. '0,1,2,3'. Applied before torch is imported.",
    )
    parser.add_argument(
        "--device-map",
        default=None,
        help=(
            "Optional transformers device_map for dense models, e.g. 'auto' for multi-GPU sharding. "
            "When set, the script does not call model.to(device)."
        ),
    )
    parser.add_argument(
        "--data-parallel",
        action="store_true",
        help="Use torch.nn.DataParallel over all visible GPUs for dense embedding models.",
    )
    parser.add_argument(
        "--torch-dtype",
        default=None,
        choices=["auto", "float32", "float16", "bfloat16"],
        help="Optional dtype for dense AutoModel loading.",
    )
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument("--bm25-k1", type=float, default=1.5)
    parser.add_argument("--bm25-b", type=float, default=0.75)
    return parser.parse_args()


def tokenize(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9_./:+#-]+", text.lower())


def row_texts(rows: list[dict[str, Any]]) -> tuple[list[str], list[str], list[str]]:
    prompts = [row["prompt"] for row in rows]
    chosen = [row["chosen"][0] for row in rows]
    rejected = [row["rejected"][0] for row in rows]
    return prompts, chosen, rejected


def load_fit_rows(paths: list[str], fallback_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not paths:
        return fallback_rows
    rows: list[dict[str, Any]] = []
    for path in paths:
        rows.extend(load_preference_rows(path))
    return rows


def tfidf_scores(
    rows: list[dict[str, Any]],
    fit_rows: list[dict[str, Any]],
) -> tuple[np.ndarray, np.ndarray]:
    prompts, chosen, rejected = row_texts(rows)
    fit_prompts, fit_chosen, fit_rejected = row_texts(fit_rows)
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1, norm="l2")
    vectorizer.fit(fit_prompts + fit_chosen + fit_rejected)
    prompt_x = vectorizer.transform(prompts)
    chosen_x = vectorizer.transform(chosen)
    rejected_x = vectorizer.transform(rejected)
    chosen_scores = np.asarray(prompt_x.multiply(chosen_x).sum(1)).ravel()
    rejected_scores = np.asarray(prompt_x.multiply(rejected_x).sum(1)).ravel()
    return chosen_scores, rejected_scores


class BM25Scorer:
    def __init__(self, documents: list[str], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.doc_tokens = [tokenize(doc) for doc in documents]
        self.doc_len = np.array([len(tokens) for tokens in self.doc_tokens], dtype=float)
        self.avgdl = float(np.mean(self.doc_len)) if len(self.doc_len) else 0.0
        self.term_freqs = [Counter(tokens) for tokens in self.doc_tokens]
        doc_freq: Counter[str] = Counter()
        for freqs in self.term_freqs:
            doc_freq.update(freqs.keys())
        total_docs = max(len(self.doc_tokens), 1)
        self.idf = {
            term: math.log(1.0 + (total_docs - freq + 0.5) / (freq + 0.5))
            for term, freq in doc_freq.items()
        }

    def score(self, query: str, document: str) -> float:
        query_terms = tokenize(query)
        freqs = Counter(tokenize(document))
        doc_len = sum(freqs.values())
        if not query_terms or doc_len == 0:
            return 0.0
        score = 0.0
        length_norm = 1.0 - self.b + self.b * (doc_len / self.avgdl if self.avgdl else 0.0)
        for term in query_terms:
            tf = freqs.get(term, 0)
            if tf <= 0:
                continue
            idf = self.idf.get(term, 0.0)
            score += idf * (tf * (self.k1 + 1.0)) / (tf + self.k1 * length_norm)
        return float(score)


def bm25_scores(
    rows: list[dict[str, Any]],
    fit_rows: list[dict[str, Any]],
    k1: float,
    b: float,
) -> tuple[np.ndarray, np.ndarray]:
    prompts, chosen, rejected = row_texts(rows)
    _, fit_chosen, fit_rejected = row_texts(fit_rows)
    scorer = BM25Scorer(fit_chosen + fit_rejected, k1=k1, b=b)
    chosen_scores = np.array([scorer.score(prompt, doc) for prompt, doc in zip(prompts, chosen)], dtype=float)
    rejected_scores = np.array([scorer.score(prompt, doc) for prompt, doc in zip(prompts, rejected)], dtype=float)
    return chosen_scores, rejected_scores


def pick_device(requested: str):
    import torch

    if requested == "cpu":
        return torch.device("cpu")
    if requested == "cuda":
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA was requested but torch cannot see a CUDA device.")
        return torch.device("cuda")
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def resolve_torch_dtype(dtype_name: str | None):
    if dtype_name is None:
        return None
    if dtype_name == "auto":
        return "auto"

    import torch

    return {
        "float32": torch.float32,
        "float16": torch.float16,
        "bfloat16": torch.bfloat16,
    }[dtype_name]


def first_parameter_device(model):
    try:
        return next(model.parameters()).device
    except StopIteration:
        return None


def mean_pool(last_hidden_state, attention_mask):
    import torch

    mask = attention_mask.unsqueeze(-1).expand(last_hidden_state.size()).float()
    return (last_hidden_state * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1e-9)


def cls_pool(last_hidden_state):
    return last_hidden_state[:, 0]


def last_token_pool(last_hidden_state, attention_mask):
    import torch

    left_padding = attention_mask[:, -1].sum() == attention_mask.shape[0]
    if left_padding:
        return last_hidden_state[:, -1]
    sequence_lengths = attention_mask.sum(dim=1) - 1
    batch_size = last_hidden_state.shape[0]
    return last_hidden_state[
        torch.arange(batch_size, device=last_hidden_state.device),
        sequence_lengths,
    ]


def pool_hidden_states(last_hidden_state, attention_mask, pooling: str):
    if pooling == "mean":
        return mean_pool(last_hidden_state, attention_mask)
    if pooling == "cls":
        return cls_pool(last_hidden_state)
    if pooling == "last_token":
        return last_token_pool(last_hidden_state, attention_mask)
    raise ValueError(f"Unsupported pooling strategy: {pooling}")


def dense_embeddings(
    texts: list[str],
    model_path: str,
    batch_size: int,
    max_length: int,
    device_name: str,
    local_files_only: bool,
    device_map: str | None,
    data_parallel: bool,
    torch_dtype: str | None,
    trust_remote_code: bool,
    pooling: str,
    progress_every: int,
) -> np.ndarray:
    import torch
    from transformers import AutoModel, AutoTokenizer

    common_kwargs = {
        "local_files_only": local_files_only,
        "trust_remote_code": trust_remote_code,
    }
    model_kwargs = dict(common_kwargs)
    resolved_dtype = resolve_torch_dtype(torch_dtype)
    if resolved_dtype is not None:
        model_kwargs["torch_dtype"] = resolved_dtype
    if device_map:
        model_kwargs["device_map"] = device_map
        model_kwargs["low_cpu_mem_usage"] = True

    tokenizer_kwargs = dict(common_kwargs)
    if pooling == "last_token":
        tokenizer_kwargs["padding_side"] = "left"
    tokenizer = AutoTokenizer.from_pretrained(model_path, **tokenizer_kwargs)
    model = AutoModel.from_pretrained(model_path, **model_kwargs)
    device = pick_device(device_name)
    if device_map:
        input_device = first_parameter_device(model) or device
    else:
        model.to(device)
        if data_parallel and device.type == "cuda":
            visible_gpus = torch.cuda.device_count()
            if visible_gpus < 2:
                raise RuntimeError("--data-parallel requested, but fewer than 2 CUDA devices are visible.")
            model = torch.nn.DataParallel(model)
        input_device = device
    model.eval()

    embeddings: list[np.ndarray] = []
    total_batches = math.ceil(len(texts) / batch_size) if batch_size else 0
    started_at = time.time()
    if progress_every > 0:
        print(
            f"[dense] encoding {len(texts)} texts in {total_batches} batches "
            f"(batch_size={batch_size}, max_length={max_length}, device={input_device})",
            file=sys.stderr,
            flush=True,
        )
    with torch.no_grad():
        for batch_index, start in enumerate(range(0, len(texts), batch_size), start=1):
            batch = texts[start : start + batch_size]
            encoded = tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=max_length,
                return_tensors="pt",
            )
            encoded = {key: value.to(input_device) for key, value in encoded.items()}
            outputs = model(**encoded)
            pooled = pool_hidden_states(outputs.last_hidden_state, encoded["attention_mask"], pooling)
            pooled = torch.nn.functional.normalize(pooled, p=2, dim=1)
            embeddings.append(pooled.float().cpu().numpy())
            if progress_every > 0 and (
                batch_index == 1
                or batch_index == total_batches
                or batch_index % progress_every == 0
            ):
                elapsed = max(time.time() - started_at, 1e-9)
                rate = batch_index / elapsed
                remaining = (total_batches - batch_index) / rate if rate > 0 else 0.0
                print(
                    f"[dense] batch {batch_index}/{total_batches} "
                    f"({100.0 * batch_index / max(total_batches, 1):.1f}%), "
                    f"elapsed={elapsed/60:.1f}m, eta={remaining/60:.1f}m",
                    file=sys.stderr,
                    flush=True,
                )
    return np.vstack(embeddings)


def dense_scores(
    rows: list[dict[str, Any]],
    method: str,
    model_path: str | None,
    batch_size: int,
    max_length: int,
    device: str,
    local_files_only: bool,
    device_map: str | None,
    data_parallel: bool,
    torch_dtype: str | None,
    trust_remote_code: bool,
    pooling: str,
    query_instruction: str | None,
    progress_every: int,
) -> tuple[np.ndarray, np.ndarray]:
    prompts, chosen, rejected = row_texts(rows)
    if model_path is None:
        model_path = DEFAULT_E5_MODEL if method == "e5" else DEFAULT_SBERT_MODEL
    if method == "e5":
        prompts = [f"query: {text}" for text in prompts]
        chosen = [f"passage: {text}" for text in chosen]
        rejected = [f"passage: {text}" for text in rejected]
    elif query_instruction:
        prompts = [f"Instruct: {query_instruction}\nQuery: {text}" for text in prompts]
    docs = prompts + chosen + rejected
    embeddings = dense_embeddings(
        docs,
        model_path=model_path,
        batch_size=batch_size,
        max_length=max_length,
        device_name=device,
        local_files_only=local_files_only,
        device_map=device_map,
        data_parallel=data_parallel,
        torch_dtype=torch_dtype,
        trust_remote_code=trust_remote_code,
        pooling=pooling,
        progress_every=progress_every,
    )
    n = len(prompts)
    prompt_e = embeddings[:n]
    chosen_e = embeddings[n : 2 * n]
    rejected_e = embeddings[2 * n :]
    chosen_scores = np.sum(prompt_e * chosen_e, axis=1)
    rejected_scores = np.sum(prompt_e * rejected_e, axis=1)
    return chosen_scores, rejected_scores


def reranker_name(model_path: str | None) -> str | None:
    if not model_path:
        return model_path
    path = Path(model_path)
    name = path.name if path.exists() else model_path
    mapping = {
        "BAAI_bge-reranker-v2-m3": "BAAI/bge-reranker-v2-m3",
        "Qwen_Qwen3-Reranker-8B": "Qwen/Qwen3-Reranker-8B",
        "jinaai_jina-reranker-v3": "jinaai/jina-reranker-v3",
    }
    return mapping.get(name, name)


def reranker_kind(model_path: str) -> str:
    name = (reranker_name(model_path) or model_path).lower()
    if "qwen3-reranker" in name:
        return "qwen3"
    if "jina-reranker-v3" in name:
        return "jina_v3"
    if "bge-reranker-v2-m3" in name:
        return "bge_v2_m3"
    raise ValueError(f"Unsupported reranker model: {model_path}")


def batched(items: list[Any], batch_size: int) -> list[list[Any]]:
    return [items[i : i + batch_size] for i in range(0, len(items), batch_size)]


def skyjury_reranker_instruction() -> str:
    return "Given a user profile, retrieve the labeler policy description that best matches the user's moderation needs."


def bge_reranker_scores(rows: list[dict[str, Any]], model_path: str, args: argparse.Namespace, device) -> list[float]:
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        local_files_only=args.local_files_only,
        trust_remote_code=args.trust_remote_code,
    )
    model_kwargs = {
        "local_files_only": args.local_files_only,
        "trust_remote_code": args.trust_remote_code,
    }
    resolved_dtype = resolve_torch_dtype(args.torch_dtype)
    if resolved_dtype is not None:
        model_kwargs["torch_dtype"] = resolved_dtype
    if args.device_map:
        model_kwargs["device_map"] = args.device_map
        model_kwargs["low_cpu_mem_usage"] = True
    model = AutoModelForSequenceClassification.from_pretrained(model_path, **model_kwargs)
    if not args.device_map:
        model.to(device)
    model.eval()

    pairs = [[row["query"], row["document"]] for row in rows]
    scores: list[float] = []
    total_batches = math.ceil(len(pairs) / args.reranker_batch_size)
    with torch.no_grad():
        for batch_index, pair_batch in enumerate(batched(pairs, args.reranker_batch_size), start=1):
            inputs = tokenizer(
                pair_batch,
                padding=True,
                truncation=True,
                return_tensors="pt",
                max_length=args.reranker_max_length,
            )
            input_device = first_parameter_device(model) or device
            inputs = {key: value.to(input_device) for key, value in inputs.items()}
            scores.extend(model(**inputs, return_dict=True).logits.view(-1).float().detach().cpu().tolist())
            if args.progress_every > 0 and (
                batch_index == 1 or batch_index == total_batches or batch_index % args.progress_every == 0
            ):
                print(f"[reranker:bge] batch {batch_index}/{total_batches}", file=sys.stderr, flush=True)
    del model
    del tokenizer
    if device.type == "cuda":
        torch.cuda.empty_cache()
    return scores


def qwen3_format_instruction(query: str, doc: str) -> str:
    return f"<Instruct>: {skyjury_reranker_instruction()}\n<Query>: {query}\n<Document>: {doc}"


def qwen3_reranker_scores(rows: list[dict[str, Any]], model_path: str, args: argparse.Namespace, device) -> list[float]:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        padding_side="left",
        trust_remote_code=True,
        local_files_only=args.local_files_only,
    )
    model_kwargs = {
        "trust_remote_code": True,
        "local_files_only": args.local_files_only,
    }
    resolved_dtype = resolve_torch_dtype(args.torch_dtype)
    if resolved_dtype is not None:
        model_kwargs["torch_dtype"] = resolved_dtype
    if args.device_map:
        model_kwargs["device_map"] = args.device_map
        model_kwargs["low_cpu_mem_usage"] = True
    model = AutoModelForCausalLM.from_pretrained(model_path, **model_kwargs).eval()
    if not args.device_map:
        model.to(device)

    token_false_id = tokenizer.convert_tokens_to_ids("no")
    token_true_id = tokenizer.convert_tokens_to_ids("yes")
    prefix = (
        "<|im_start|>system\n"
        'Judge whether the Document meets the requirements based on the Query and the Instruct provided. '
        'Note that the answer can only be "yes" or "no".<|im_end|>\n'
        "<|im_start|>user\n"
    )
    suffix = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
    prefix_tokens = tokenizer.encode(prefix, add_special_tokens=False)
    suffix_tokens = tokenizer.encode(suffix, add_special_tokens=False)
    max_pair_length = args.reranker_max_length - len(prefix_tokens) - len(suffix_tokens)
    if max_pair_length <= 0:
        raise ValueError("--reranker-max-length is too small for Qwen3 reranker prefix/suffix.")

    pairs = [qwen3_format_instruction(row["query"], row["document"]) for row in rows]
    scores: list[float] = []
    total_batches = math.ceil(len(pairs) / args.reranker_batch_size)
    with torch.no_grad():
        for batch_index, pair_batch in enumerate(batched(pairs, args.reranker_batch_size), start=1):
            inputs = tokenizer(
                pair_batch,
                padding=False,
                truncation="longest_first",
                return_attention_mask=False,
                max_length=max_pair_length,
            )
            for i, input_ids in enumerate(inputs["input_ids"]):
                inputs["input_ids"][i] = prefix_tokens + input_ids + suffix_tokens
            padded = tokenizer.pad(inputs, padding=True, return_tensors="pt", max_length=args.reranker_max_length)
            input_device = first_parameter_device(model) or device
            padded = {key: value.to(input_device) for key, value in padded.items()}
            batch_logits = model(**padded).logits[:, -1, :]
            true_vector = batch_logits[:, token_true_id]
            false_vector = batch_logits[:, token_false_id]
            yes_no = torch.stack([false_vector, true_vector], dim=1)
            scores.extend(torch.nn.functional.log_softmax(yes_no, dim=1)[:, 1].exp().detach().cpu().tolist())
            if args.progress_every > 0 and (
                batch_index == 1 or batch_index == total_batches or batch_index % args.progress_every == 0
            ):
                print(f"[reranker:qwen3] batch {batch_index}/{total_batches}", file=sys.stderr, flush=True)
    del model
    del tokenizer
    if device.type == "cuda":
        torch.cuda.empty_cache()
    return scores


def jina_v3_reranker_scores(rows: list[dict[str, Any]], model_path: str, args: argparse.Namespace, device) -> list[float]:
    import torch
    from transformers import AutoModel

    model_kwargs = {
        "trust_remote_code": True,
        "local_files_only": args.local_files_only,
    }
    resolved_dtype = resolve_torch_dtype(args.torch_dtype)
    if resolved_dtype is not None:
        model_kwargs["torch_dtype"] = resolved_dtype
    if args.device_map:
        model_kwargs["device_map"] = args.device_map
        model_kwargs["low_cpu_mem_usage"] = True
    model = AutoModel.from_pretrained(model_path, **model_kwargs).eval()
    if not args.device_map:
        model.to(device)

    scores: list[float] = []
    total_batches = math.ceil(len(rows) / args.reranker_batch_size)
    with torch.no_grad():
        for batch_index, row_batch in enumerate(batched(rows, args.reranker_batch_size), start=1):
            for row in row_batch:
                result = model.rerank(row["query"], [row["document"]], top_n=None, return_embeddings=False)[0]
                scores.append(float(result["relevance_score"]))
            if args.progress_every > 0 and (
                batch_index == 1 or batch_index == total_batches or batch_index % args.progress_every == 0
            ):
                print(f"[reranker:jina-v3] batch {batch_index}/{total_batches}", file=sys.stderr, flush=True)
    del model
    if device.type == "cuda":
        torch.cuda.empty_cache()
    return scores


def reranker_scores(rows: list[dict[str, Any]], model_path: str, args: argparse.Namespace, device) -> list[float]:
    kind = reranker_kind(model_path)
    if kind == "bge_v2_m3":
        return bge_reranker_scores(rows, model_path, args, device)
    if kind == "qwen3":
        return qwen3_reranker_scores(rows, model_path, args, device)
    if kind == "jina_v3":
        return jina_v3_reranker_scores(rows, model_path, args, device)
    raise AssertionError(f"Unhandled reranker kind: {kind}")


def jina_v3_skyjury_pair_scores(
    rows: list[dict[str, Any]],
    model_path: str,
    args: argparse.Namespace,
    device,
) -> tuple[np.ndarray, np.ndarray]:
    import torch
    from transformers import AutoModel

    model_kwargs = {
        "trust_remote_code": True,
        "local_files_only": args.local_files_only,
    }
    resolved_dtype = resolve_torch_dtype(args.torch_dtype)
    if resolved_dtype is not None:
        model_kwargs["torch_dtype"] = resolved_dtype
    if args.device_map:
        model_kwargs["device_map"] = args.device_map
        model_kwargs["low_cpu_mem_usage"] = True
    model = AutoModel.from_pretrained(model_path, **model_kwargs).eval()
    if not args.device_map:
        model.to(device)

    chosen_scores: list[float] = []
    rejected_scores: list[float] = []
    total = len(rows)
    with torch.no_grad():
        for index, row in enumerate(rows, start=1):
            documents = [row["chosen"][0], row["rejected"][0]]
            results = model.rerank(row["prompt"], documents, top_n=None, return_embeddings=False)
            scores = {int(result["index"]): float(result["relevance_score"]) for result in results}
            chosen_scores.append(scores[0])
            rejected_scores.append(scores[1])
            if args.progress_every > 0 and (
                index == 1 or index == total or index % args.progress_every == 0
            ):
                print(f"[reranker:jina-v3] pair {index}/{total}", file=sys.stderr, flush=True)
    del model
    if device.type == "cuda":
        torch.cuda.empty_cache()
    return np.asarray(chosen_scores, dtype=float), np.asarray(rejected_scores, dtype=float)


def skyjury_reranker_rows(rows: list[dict[str, Any]], side: str) -> list[dict[str, Any]]:
    if side not in {"chosen", "rejected"}:
        raise ValueError(f"Unsupported side: {side}")
    reranker_rows = []
    for row in rows:
        labeler_text = row[side][0]
        reranker_rows.append(
            {
                "category": "SkyJury",
                "task": row.get("subset", "labeler_selection"),
                "split": "",
                "id": row.get("id", ""),
                "query": row["prompt"],
                "document": labeler_text,
                "score": None,
                "label": None,
            }
        )
    return reranker_rows


def direct_reranker_pair_scores(
    rows: list[dict[str, Any]],
    model_path: str,
    args: argparse.Namespace,
    device_name: str,
) -> tuple[np.ndarray, np.ndarray]:
    if not model_path:
        raise ValueError("--model-path is required when --method reranker.")
    device = pick_device(device_name)
    args.reranker_batch_size = args.reranker_batch_size or args.batch_size
    args.reranker_max_length = args.reranker_max_length or args.max_length
    if reranker_kind(model_path) == "jina_v3":
        return jina_v3_skyjury_pair_scores(rows, model_path, args, device)
    chosen = reranker_scores(skyjury_reranker_rows(rows, "chosen"), model_path, args, device)
    rejected = reranker_scores(skyjury_reranker_rows(rows, "rejected"), model_path, args, device)
    return np.asarray(chosen, dtype=float), np.asarray(rejected, dtype=float)


def attach_scores(rows: list[dict[str, Any]], chosen_scores: np.ndarray, rejected_scores: np.ndarray) -> None:
    for row, chosen_score, rejected_score in zip(rows, chosen_scores, rejected_scores):
        row["score_chosen"] = [float(chosen_score)]
        row["score_rejected"] = [float(rejected_score)]


def main() -> None:
    args = parse_args()
    if args.cuda_devices:
        os.environ["CUDA_VISIBLE_DEVICES"] = args.cuda_devices
    rows = load_preference_rows(args.data, limit=args.limit)
    fit_rows = load_fit_rows(args.fit_data, fallback_rows=rows)

    if args.method == "tfidf":
        chosen_scores, rejected_scores = tfidf_scores(rows, fit_rows)
    elif args.method == "bm25":
        chosen_scores, rejected_scores = bm25_scores(rows, fit_rows, k1=args.bm25_k1, b=args.bm25_b)
    elif args.method in {"sbert", "e5"}:
        chosen_scores, rejected_scores = dense_scores(
            rows,
            method=args.method,
            model_path=args.model_path,
            batch_size=args.batch_size,
            max_length=args.max_length,
            device=args.device,
            local_files_only=args.local_files_only,
            device_map=args.device_map,
            data_parallel=args.data_parallel,
            torch_dtype=args.torch_dtype,
            trust_remote_code=args.trust_remote_code,
            pooling=args.pooling,
            query_instruction=args.query_instruction,
            progress_every=args.progress_every,
        )
    elif args.method == "reranker":
        chosen_scores, rejected_scores = direct_reranker_pair_scores(
            rows,
            model_path=args.model_path,
            args=args,
            device_name=args.device,
        )
    else:
        raise ValueError(f"Unsupported method: {args.method}")

    attach_scores(rows, chosen_scores, rejected_scores)
    metrics = compute_accuracy(rows)
    metrics.update(
        {
            "method": f"similarity_{args.method}",
            "similarity_method": args.method,
            "model": args.model_path,
            "model_name": reranker_name(args.model_path) if args.method == "reranker" and args.model_path else args.model_path,
            "device": args.device,
            "cuda_devices": args.cuda_devices,
            "device_map": args.device_map,
            "data_parallel": args.data_parallel,
            "torch_dtype": args.torch_dtype,
            "trust_remote_code": args.trust_remote_code,
            "pooling": args.pooling,
            "query_instruction": args.query_instruction,
            "progress_every": args.progress_every,
            "fit_data": args.fit_data or [args.data],
            "score_definition": "reranker_score(user_profile, labeler_text)" if args.method == "reranker" else "similarity(user_profile, labeler_text)",
            "mean_chosen_score": float(np.mean(chosen_scores)),
            "mean_rejected_score": float(np.mean(rejected_scores)),
            "mean_margin": float(np.mean(chosen_scores - rejected_scores)),
            "median_margin": float(np.median(chosen_scores - rejected_scores)),
        }
    )
    model_name = args.model_path or args.method
    result_path, metrics_path = write_result_bundle(
        rows=rows,
        metrics=metrics,
        output_dir=args.output_dir,
        dataset_path=args.data,
        model_name=model_name,
        method=f"similarity_{args.method}",
    )
    print(f"accuracy={metrics['accuracy']:.4f} ({metrics['correct_pairs']}/{metrics['total_pairs']})")
    print(f"predictions={result_path}")
    print(f"metrics={metrics_path}")


if __name__ == "__main__":
    main()
