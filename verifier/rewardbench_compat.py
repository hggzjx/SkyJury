from __future__ import annotations

import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import torch
from tqdm import tqdm
from transformers import AutoModel, AutoModelForCausalLM, AutoModelForSequenceClassification, AutoTokenizer


@dataclass(frozen=True)
class RewardModelConfig:
    model_builder: str = "sequence_classification"
    trust_remote_code: bool = False
    torch_dtype: str | None = None
    tokenizer_padding_side: str = "left"
    tokenizer_truncation_side: str = "right"
    tokenizer_source: str | None = None
    attn_implementation: str | None = None
    num_labels: int | None = None
    reward_score_index: int | None = None
    add_special_tokens: bool = True
    tokenize_chat_template: bool = False


@dataclass(frozen=True)
class DPOModelConfig:
    model_builder: str = "causal_lm"
    tokenizer_builder: str = "auto"
    trust_remote_code: bool = False


REWARD_MODEL_CONFIG: dict[str, RewardModelConfig] = {
    "default": RewardModelConfig(),
    "OpenAssistant/reward-model-deberta-v3-large-v2": RewardModelConfig(),
    "RLHFlow/ArmoRM-Llama3-8B-v0.1": RewardModelConfig(
        trust_remote_code=True,
        tokenizer_padding_side="left",
        tokenizer_truncation_side="right",
    ),
    "Ray2333/GRM_Llama3.1_8B_rewardmodel-ft": RewardModelConfig(
        tokenizer_source="/ssd1/lbh/zjx/models/skyjury_verifier/RLHFlow_ArmoRM-Llama3-8B-v0.1",
    ),
    "Skywork/Skywork-Reward-Gemma-2-27B-v0.2": RewardModelConfig(
        torch_dtype="bfloat16",
        attn_implementation="eager",
        num_labels=1,
        reward_score_index=0,
        add_special_tokens=False,
        tokenize_chat_template=True,
    ),
    "openbmb/Eurus-RM-7b": RewardModelConfig(
        model_builder="auto_model",
        trust_remote_code=True,
        torch_dtype="bfloat16",
    ),
}


DPO_MODEL_CONFIG: dict[str, DPOModelConfig] = {
    "default": DPOModelConfig(),
    "allenai/tulu-2-dpo-7b": DPOModelConfig(),
    "allenai/tulu-2-dpo-13b": DPOModelConfig(),
    "HuggingFaceH4/zephyr-7b-beta": DPOModelConfig(),
    "upstage/SOLAR-10.7B-Instruct-v1.0": DPOModelConfig(),
}


LOCAL_MODEL_ALIASES = {
    "OpenAssistant_reward-model-deberta-v3-large-v2": "OpenAssistant/reward-model-deberta-v3-large-v2",
    "RLHFlow_ArmoRM-Llama3-8B-v0.1": "RLHFlow/ArmoRM-Llama3-8B-v0.1",
    "Ray2333_GRM_Llama3.1_8B_rewardmodel-ft": "Ray2333/GRM_Llama3.1_8B_rewardmodel-ft",
    "Skywork_Skywork-Reward-Gemma-2-27B-v0.2": "Skywork/Skywork-Reward-Gemma-2-27B-v0.2",
    "openbmb_Eurus-RM-7b": "openbmb/Eurus-RM-7b",
    "allenai_tulu-2-dpo-7b": "allenai/tulu-2-dpo-7b",
    "allenai_tulu-2-dpo-13b": "allenai/tulu-2-dpo-13b",
    "HuggingFaceH4_zephyr-7b-beta": "HuggingFaceH4/zephyr-7b-beta",
    "upstage_SOLAR-10.7B-Instruct-v1.0": "upstage/SOLAR-10.7B-Instruct-v1.0",
}


def official_model_name(model: str) -> str:
    path_name = Path(model).name
    if path_name in LOCAL_MODEL_ALIASES:
        return LOCAL_MODEL_ALIASES[path_name]
    if model in REWARD_MODEL_CONFIG or model in DPO_MODEL_CONFIG:
        return model
    normalized = model.strip("/")
    for local_name, official in LOCAL_MODEL_ALIASES.items():
        if normalized.endswith(local_name):
            return official
    return model


def torch_dtype_from_name(name: str | None, device: torch.device) -> torch.dtype | None:
    if name is None or name == "auto":
        return torch.float16 if device.type == "cuda" else None
    return {
        "float16": torch.float16,
        "bfloat16": torch.bfloat16,
        "float32": torch.float32,
        "float64": torch.float64,
    }[name]


def pick_device(requested: str) -> torch.device:
    if requested == "cpu":
        return torch.device("cpu")
    if requested == "cuda":
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA was requested but torch cannot see a CUDA device.")
        return torch.device("cuda")
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def resolve_torch_dtype_name(requested: str | None, configured: str | None) -> str:
    if requested is None or requested == "auto":
        return configured or "auto"
    return requested


def load_tokenizer(
    model: str,
    trust_remote_code: bool,
    local_files_only: bool,
    padding_side: str = "left",
    truncation_side: str = "left",
):
    tokenizer = AutoTokenizer.from_pretrained(
        model,
        trust_remote_code=trust_remote_code,
        local_files_only=local_files_only,
    )
    tokenizer.padding_side = padding_side
    tokenizer.truncation_side = truncation_side
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token or tokenizer.unk_token
    if getattr(tokenizer, "bos_token_id", None) is None and getattr(tokenizer, "eos_token_id", None) is not None:
        tokenizer.bos_token_id = tokenizer.eos_token_id
    return tokenizer


def format_rewardbench_pair_text(tokenizer: Any, prompt: str, answer: str) -> str:
    messages = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": answer},
    ]
    if hasattr(tokenizer, "apply_chat_template") and getattr(tokenizer, "chat_template", None):
        return tokenizer.apply_chat_template(messages, tokenize=False)
    return f"<|user|>\n{prompt}\n<|assistant|>\n{answer}"


def format_rewardbench_prompt(tokenizer: Any, prompt: str) -> str:
    messages = [{"role": "user", "content": prompt}]
    if hasattr(tokenizer, "apply_chat_template") and getattr(tokenizer, "chat_template", None):
        return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    return f"<|user|>\n{prompt}\n<|assistant|>\n"


def model_kwargs(
    device: torch.device,
    dtype: torch.dtype | None,
    trust_remote_code: bool,
    local_files_only: bool,
    device_map: str | None,
    config: RewardModelConfig | None = None,
) -> dict[str, Any]:
    kwargs: dict[str, Any] = {
        "trust_remote_code": trust_remote_code,
        "local_files_only": local_files_only,
    }
    if dtype is not None:
        kwargs["torch_dtype"] = dtype
    if device.type == "cuda" and normalized_device_map(device_map) is not None:
        kwargs["device_map"] = device_map or "auto"
    if config is not None:
        if config.attn_implementation is not None:
            kwargs["attn_implementation"] = config.attn_implementation
        if config.num_labels is not None:
            kwargs["num_labels"] = config.num_labels
    return kwargs


def normalized_device_map(device_map: str | None) -> str | None:
    if device_map is None:
        return "auto"
    normalized = device_map.strip().lower()
    if normalized in {"", "none", "null", "false"}:
        return None
    return device_map


def load_reward_model(
    model: str,
    device: torch.device,
    torch_dtype_name: str | None,
    trust_remote_code: bool | None,
    local_files_only: bool,
    device_map: str | None = None,
):
    official = official_model_name(model)
    config = REWARD_MODEL_CONFIG.get(official, REWARD_MODEL_CONFIG["default"])
    effective_trust = config.trust_remote_code if trust_remote_code is None else trust_remote_code
    dtype = torch_dtype_from_name(resolve_torch_dtype_name(torch_dtype_name, config.torch_dtype), device)
    kwargs = model_kwargs(device, dtype, effective_trust, local_files_only, device_map, config)
    if config.model_builder == "auto_model":
        loaded = AutoModel.from_pretrained(model, **kwargs)
    else:
        loaded = AutoModelForSequenceClassification.from_pretrained(model, **kwargs)
    if device.type == "cpu" or (device.type == "cuda" and "device_map" not in kwargs):
        loaded.to(device)
    loaded.eval()
    return loaded, config, effective_trust


def extract_reward_scores(
    outputs: Any,
    attention_mask: torch.Tensor | None = None,
    score_index: int | None = None,
) -> torch.Tensor:
    if isinstance(outputs, torch.Tensor):
        tensor = outputs
    elif hasattr(outputs, "logits") and outputs.logits is not None:
        tensor = outputs.logits
    elif hasattr(outputs, "score") and outputs.score is not None:
        tensor = outputs.score
    elif hasattr(outputs, "rewards") and outputs.rewards is not None:
        tensor = outputs.rewards
    elif isinstance(outputs, dict):
        for key in ("logits", "score", "rewards"):
            if key in outputs and outputs[key] is not None:
                tensor = outputs[key]
                break
        else:
            raise ValueError(f"Cannot extract reward score from output keys: {list(outputs.keys())}")
    elif isinstance(outputs, (tuple, list)) and outputs:
        tensor = outputs[0]
    else:
        raise ValueError(f"Cannot extract reward score from output type: {type(outputs).__name__}")

    if tensor.ndim == 0:
        return tensor.reshape(1)
    if tensor.ndim == 1:
        return tensor
    if tensor.ndim == 2:
        if tensor.shape[-1] == 1:
            return tensor.squeeze(-1)
        if attention_mask is not None and tensor.shape[1] == attention_mask.shape[1]:
            lengths = attention_mask.long().sum(dim=1).clamp(min=1) - 1
            return tensor[torch.arange(tensor.shape[0], device=tensor.device), lengths]
        if score_index is not None:
            return tensor[:, score_index]
        return tensor[:, -1]
    return tensor.reshape(tensor.shape[0], -1)[:, -1]


def score_reward_texts(
    model: torch.nn.Module,
    tokenizer: Any,
    texts: list[str],
    batch_size: int,
    max_length: int,
    device: torch.device,
    score_index: int | None = None,
    add_special_tokens: bool = True,
) -> list[float]:
    scores: list[float] = []
    with torch.inference_mode():
        for start in tqdm(range(0, len(texts), batch_size), desc="RewardBench RM scoring"):
            batch = texts[start : start + batch_size]
            encoded = tokenizer(
                batch,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=max_length,
                add_special_tokens=add_special_tokens,
            )
            encoded = {key: value.to(device if device.type == "cuda" else "cpu") for key, value in encoded.items()}
            outputs = model(**encoded)
            batch_scores = extract_reward_scores(outputs, encoded.get("attention_mask"), score_index)
            scores.extend(batch_scores.detach().float().cpu().tolist())
    return scores


def score_reward_conversations(
    model: torch.nn.Module,
    tokenizer: Any,
    conversations: list[list[dict[str, str]]],
    max_length: int,
    device: torch.device,
    score_index: int | None = None,
) -> list[float]:
    scores: list[float] = []
    with torch.inference_mode():
        for conversation in tqdm(conversations, desc="RewardBench RM chat-template scoring"):
            encoded = tokenizer.apply_chat_template(
                conversation,
                tokenize=True,
                return_tensors="pt",
                truncation=True,
                max_length=max_length,
            )
            if isinstance(encoded, dict):
                model_inputs = {
                    key: value.to(device if device.type == "cuda" else "cpu")
                    for key, value in encoded.items()
                    if isinstance(value, torch.Tensor)
                }
                attention_mask = model_inputs.get("attention_mask")
            else:
                model_inputs = {"input_ids": encoded.to(device if device.type == "cuda" else "cpu")}
                attention_mask = None
            outputs = model(**model_inputs)
            score = extract_reward_scores(outputs, attention_mask, score_index)
            scores.extend(score.detach().float().cpu().tolist())
    return scores


def load_causal_lm(
    model: str,
    device: torch.device,
    torch_dtype_name: str | None,
    trust_remote_code: bool,
    local_files_only: bool,
    device_map: str | None = None,
):
    dtype = torch_dtype_from_name(torch_dtype_name or "auto", device)
    kwargs = model_kwargs(device, dtype, trust_remote_code, local_files_only, device_map)
    loaded = AutoModelForCausalLM.from_pretrained(model, **kwargs)
    if device.type == "cpu" or (device.type == "cuda" and "device_map" not in kwargs):
        loaded.to(device)
    loaded.eval()
    return loaded


def sequence_logprob(
    model: torch.nn.Module,
    input_ids: torch.Tensor,
    attention_mask: torch.Tensor,
    labels: torch.Tensor,
    reduction: Literal["sum", "avg", "norm"] = "avg",
) -> torch.Tensor:
    outputs = model(input_ids=input_ids, attention_mask=attention_mask)
    logits = outputs.logits[:, :-1, :]
    shifted_labels = labels[:, 1:]
    shifted_mask = shifted_labels.ne(-100)
    safe_labels = shifted_labels.masked_fill(~shifted_mask, 0)
    log_probs = torch.log_softmax(logits, dim=-1)
    token_log_probs = log_probs.gather(-1, safe_labels.unsqueeze(-1)).squeeze(-1)
    token_log_probs = token_log_probs * shifted_mask
    summed = token_log_probs.sum(dim=1)
    lengths = shifted_mask.sum(dim=1).clamp(min=1)
    if reduction == "sum":
        return summed
    if reduction == "norm":
        return -torch.norm(token_log_probs, p=2, dim=-1)
    return summed / lengths.float()


def build_tokenized_answer(tokenizer: Any, prompt: str, answer: str) -> dict[str, list[int]]:
    full_tokenized = tokenizer(prompt + answer, add_special_tokens=False)
    prompt_tokenized = tokenizer(prompt, add_special_tokens=False)
    prompt_input_ids = prompt_tokenized["input_ids"]
    response_start = len(prompt_input_ids)
    if prompt_input_ids != full_tokenized["input_ids"][:response_start]:
        response_start -= 1
    return {
        "prompt_input_ids": full_tokenized["input_ids"][:response_start],
        "prompt_attention_mask": full_tokenized["attention_mask"][:response_start],
        "input_ids": full_tokenized["input_ids"][response_start:],
        "attention_mask": full_tokenized["attention_mask"][response_start:],
    }


def encode_prompt_answer(
    tokenizer: Any,
    prompt: str,
    answer: str,
    max_length: int,
    max_prompt_length: int,
) -> dict[str, list[int]]:
    prefix = format_rewardbench_prompt(tokenizer, prompt)
    tokens = build_tokenized_answer(tokenizer, prefix, answer)
    prompt_ids = tokens["prompt_input_ids"]
    prompt_mask = tokens["prompt_attention_mask"]
    answer_ids = tokens["input_ids"]
    answer_mask = tokens["attention_mask"]

    if tokenizer.bos_token_id is not None and (not prompt_ids or prompt_ids[0] != tokenizer.bos_token_id):
        prompt_ids = [tokenizer.bos_token_id] + prompt_ids
        prompt_mask = [1] + prompt_mask
    if tokenizer.eos_token_id is not None and (not answer_ids or answer_ids[-1] != tokenizer.eos_token_id):
        answer_ids = answer_ids + [tokenizer.eos_token_id]
        answer_mask = answer_mask + [1]

    if len(prompt_ids) + len(answer_ids) > max_length:
        prompt_ids = prompt_ids[-max_prompt_length:]
        prompt_mask = prompt_mask[-max_prompt_length:]
    if len(prompt_ids) + len(answer_ids) > max_length:
        answer_budget = max(1, max_length - len(prompt_ids))
        answer_ids = answer_ids[:answer_budget]
        answer_mask = answer_mask[:answer_budget]

    input_ids = prompt_ids + answer_ids
    attention_mask = prompt_mask + answer_mask
    prompt_len = len(prompt_ids)
    labels = list(input_ids)
    labels[:prompt_len] = [-100] * prompt_len
    return {"input_ids": input_ids, "attention_mask": attention_mask, "labels": labels}


def collate_lm_features(features: list[dict[str, list[int]]], pad_token_id: int, label_pad_token_id: int = -100):
    max_len = max(len(feature["input_ids"]) for feature in features)
    input_ids = []
    attention_mask = []
    labels = []
    for feature in features:
        pad_len = max_len - len(feature["input_ids"])
        input_ids.append(feature["input_ids"] + [pad_token_id] * pad_len)
        attention_mask.append(feature["attention_mask"] + [0] * pad_len)
        labels.append(feature["labels"] + [label_pad_token_id] * pad_len)
    return {
        "input_ids": torch.tensor(input_ids, dtype=torch.long),
        "attention_mask": torch.tensor(attention_mask, dtype=torch.long),
        "labels": torch.tensor(labels, dtype=torch.long),
    }


def score_dpo_pairs(
    model: torch.nn.Module,
    ref_model: torch.nn.Module | None,
    tokenizer: Any,
    rows: list[dict[str, Any]],
    batch_size: int,
    max_length: int,
    device: torch.device,
    max_prompt_length: int = 1024,
    reduction: Literal["sum", "avg", "norm"] = "avg",
) -> tuple[list[list[float]], list[list[float]]]:
    flat: list[tuple[int, str, dict[str, list[int]]]] = []
    for row_idx, row in enumerate(rows):
        for answer in row["chosen"]:
            flat.append(
                (
                    row_idx,
                    "chosen",
                    encode_prompt_answer(tokenizer, row["prompt"], answer, max_length, max_prompt_length),
                )
            )
        for answer in row["rejected"]:
            flat.append(
                (
                    row_idx,
                    "rejected",
                    encode_prompt_answer(tokenizer, row["prompt"], answer, max_length, max_prompt_length),
                )
            )

    chosen_scores = [[] for _ in rows]
    rejected_scores = [[] for _ in rows]
    pad_token_id = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id
    if pad_token_id is None:
        raise ValueError("Tokenizer must have a pad_token_id or eos_token_id for DPO scoring.")

    with torch.inference_mode():
        for start in tqdm(range(0, len(flat), batch_size), desc="RewardBench DPO scoring"):
            batch_items = flat[start : start + batch_size]
            batch = collate_lm_features([item[2] for item in batch_items], pad_token_id)
            batch = {key: value.to(device if device.type == "cuda" else "cpu") for key, value in batch.items()}
            effective_reduction = "sum" if ref_model is not None else reduction
            policy_scores = sequence_logprob(
                model,
                batch["input_ids"],
                batch["attention_mask"],
                batch["labels"],
                reduction=effective_reduction,
            )
            if ref_model is not None:
                ref_scores = sequence_logprob(
                    ref_model,
                    batch["input_ids"],
                    batch["attention_mask"],
                    batch["labels"],
                    reduction=effective_reduction,
                )
                batch_scores = policy_scores - ref_scores
            else:
                batch_scores = policy_scores

            for (row_idx, side, _), score in zip(batch_items, batch_scores.detach().float().cpu().tolist()):
                if side == "chosen":
                    chosen_scores[row_idx].append(float(score))
                else:
                    rejected_scores[row_idx].append(float(score))
    return chosen_scores, rejected_scores
