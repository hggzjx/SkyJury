from __future__ import annotations

import argparse
import http.client
import json
import os
import random
import socket
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from tqdm import tqdm

from utils import compute_accuracy, load_preference_rows, write_result_bundle


DEFAULT_DATA = "/ssd1/lbh/zjx/skyjury/data/skyjury_bench.json"
DEFAULT_BASE_URL = "https://api.chatanywhere.tech/v1/"


class EmptyJudgeResponseError(ValueError):
    pass


SYSTEM_PROMPT = """你是一个严格的偏好判断器。你的任务是根据用户画像和行为上下文，判断两个 Bluesky Labeler 候选项中哪一个更适合推荐给该用户。

请只依据：
1. 用户的真实需求；
2. 候选 Labeler 的描述；
3. 候选 Labeler 的 rubrics / label definitions。

不要因为某个候选更长、更泛化、看起来更安全、或关键词更多就自动选择它。你必须判断哪一个候选更贴合用户当前需求。
不要受候选项位置影响：A 和 B 的顺序没有任何含义，不能因为某个候选排在前面或后面而选择它。
即使两个候选都部分相关，也必须选择更适合推荐给该用户的一个。
不要展示推理过程，不要先分析，不要解释，直接给最终 JSON 结果。

你必须输出 JSON，不要输出 Markdown，不要输出额外解释。格式如下：
{"winner":"A"}

winner 只能是 "A" 或 "B"。禁止输出 "tie"、"both"、"neither" 或其他值。
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate SkyJury with an OpenAI-compatible LLM-as-judge API.")
    parser.add_argument("--model", default="gpt-4o-mini", help="Closed/open generative model name served by the API.")
    parser.add_argument("--data", default=DEFAULT_DATA, help="RM-Bench-style SkyJury preference JSON.")
    parser.add_argument("--output-dir", default="/ssd1/lbh/zjx/skyjury/verifier/results")
    parser.add_argument("--api-key", default=None, help="API key. Prefer env vars instead of passing this.")
    parser.add_argument("--base-url", default=None, help="OpenAI-compatible base URL, e.g. https://api.example.com/v1")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=1024)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--retry-sleep", type=float, default=2.0)
    parser.add_argument(
        "--concurrency",
        type=int,
        default=1,
        help="Number of samples to evaluate concurrently for API-based judging.",
    )
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument(
        "--order",
        choices=["normal", "swapped", "random", "bidirectional"],
        default="bidirectional",
        help="Candidate order strategy. bidirectional evaluates both candidate orders to reduce position bias.",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=1,
        help="Number of repeated response samples per candidate pair. With --order bidirectional, each sample runs both orders.",
    )
    parser.add_argument("--seed", type=int, default=13)
    parser.add_argument(
        "--reasoning-effort",
        default="minimal",
        help="Best-effort reasoning control for compatible OpenAI-style reasoning models.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the first judge prompt and exit.")
    return parser.parse_args()


def load_local_env() -> None:
    verifier_dir = Path(__file__).resolve().parent
    candidate_paths = [
        verifier_dir.parent / ".env",
        verifier_dir / ".env",
    ]
    env_path = next((path for path in candidate_paths if path.exists()), None)
    if env_path is None:
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def get_api_key(cli_key: str | None) -> str:
    key = cli_key or os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY_CONF")
    if not key:
        raise RuntimeError("Missing API key. Set OPENAI_API_KEY or OPENAI_API_KEY_CONF.")
    return key


def get_base_url(cli_base_url: str | None) -> str:
    return (
        cli_base_url
        or os.getenv("OPENAI_BASE_URL")
        or os.getenv("OPENAI_BASE_URL_CONF")
        or DEFAULT_BASE_URL
    ).rstrip("/")


def build_user_prompt(user_context: str, candidate_a: str, candidate_b: str) -> str:
    return f"""请判断哪个 Bluesky Labeler 更适合推荐给该用户。

<用户画像和行为上下文>
{user_context}
</用户画像和行为上下文>

<候选 Labeler A>
{candidate_a}
</候选 Labeler A>

<候选 Labeler B>
{candidate_b}
</候选 Labeler B>

请输出 JSON：
{{"winner":"A"}}

winner 必须且只能是 "A" 或 "B"。不要输出平局，不要解释。
不要写思考过程，直接输出最终 JSON。
"""


def post_chat_completion(
    base_url: str,
    api_key: str,
    model: str,
    messages: list[dict[str, str]],
    temperature: float,
    max_tokens: int,
    timeout: int,
    reasoning_effort: str | None,
) -> str:
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if reasoning_effort and model.startswith("gpt-5"):
        payload["reasoning_effort"] = reasoning_effort
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = json.loads(response.read().decode("utf-8"))
    return body["choices"][0]["message"]["content"]


def parse_judge_response(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if not cleaned:
        raise EmptyJudgeResponseError("Empty judge response")
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON judge response: {cleaned[:120]!r}") from exc
    winner = str(data.get("winner", "")).strip().upper()
    if winner not in {"A", "B"}:
        raise ValueError(f"Invalid judge winner: {winner!r}")
    return {
        "winner": winner,
        "raw": text,
    }


def call_with_retries(
    args: argparse.Namespace,
    base_url: str,
    api_key: str,
    messages: list[dict[str, str]],
) -> dict[str, Any]:
    last_error: Exception | None = None
    for attempt in range(args.retries):
        try:
            raw = post_chat_completion(
                base_url=base_url,
                api_key=api_key,
                model=args.model,
                messages=messages,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                timeout=args.timeout,
                reasoning_effort=args.reasoning_effort,
            )
            return parse_judge_response(raw)
        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            TimeoutError,
            socket.timeout,
            ConnectionError,
            http.client.RemoteDisconnected,
            http.client.HTTPException,
            ValueError,
        ) as exc:
            last_error = exc
            if attempt + 1 < args.retries:
                time.sleep(args.retry_sleep * (attempt + 1))
    if isinstance(last_error, EmptyJudgeResponseError):
        raise last_error
    raise RuntimeError(f"LLM judge API failed after {args.retries} attempts: {last_error}")


def order_plan(order: str, rng: random.Random) -> list[bool]:
    if order == "normal":
        return [False]
    if order == "swapped":
        return [True]
    if order == "random":
        return [rng.choice([False, True])]
    return [False, True]


def evaluate_row(
    row: dict[str, Any],
    row_index: int,
    args: argparse.Namespace,
    base_url: str,
    api_key: str,
) -> dict[str, Any]:
    rng = random.Random(args.seed + row_index)
    row["score_chosen"] = []
    row["score_rejected"] = []
    row["judge_calls"] = []

    for chosen_text, rejected_text in zip(row["chosen"], row["rejected"]):
        chosen_votes = 0.0
        rejected_votes = 0.0
        total_votes = 0.0
        calls = []
        for sample_index in range(args.samples):
            for swapped in order_plan(args.order, rng):
                candidate_a = rejected_text if swapped else chosen_text
                candidate_b = chosen_text if swapped else rejected_text
                user_prompt = build_user_prompt(row["prompt"], candidate_a, candidate_b)
                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ]
                try:
                    parsed = call_with_retries(args, base_url, api_key, messages)
                except Exception as exc:
                    row["skipped"] = True
                    row["skip_reason"] = str(exc)
                    row["score_chosen"] = []
                    row["score_rejected"] = []
                    row["judge_calls"] = [
                        {
                            "sample_index": sample_index,
                            "swapped": swapped,
                            "winner": None,
                            "raw": "",
                            "skipped": True,
                            "error": str(exc),
                        }
                    ]
                    return row

                if (parsed["winner"] == "A" and not swapped) or (parsed["winner"] == "B" and swapped):
                    chosen_votes += 1.0
                else:
                    rejected_votes += 1.0
                total_votes += 1.0

                calls.append(
                    {
                        "sample_index": sample_index,
                        "swapped": swapped,
                        "winner": parsed["winner"],
                        "raw": parsed["raw"],
                    }
                )

        row["score_chosen"].append(chosen_votes / total_votes)
        row["score_rejected"].append(rejected_votes / total_votes)
        row["judge_calls"].append(calls)

    return row


def main() -> None:
    load_local_env()
    args = parse_args()
    rows = load_preference_rows(args.data, limit=args.limit)

    if args.dry_run:
        first = rows[0]
        prompt = build_user_prompt(first["prompt"], first["chosen"][0], first["rejected"][0])
        print("SYSTEM PROMPT:\n")
        print(SYSTEM_PROMPT)
        print("\nUSER PROMPT:\n")
        print(prompt)
        return

    api_key = get_api_key(args.api_key)
    base_url = get_base_url(args.base_url)

    if args.concurrency < 1:
        raise ValueError("--concurrency must be >= 1")
    if args.samples < 1:
        raise ValueError("--samples must be >= 1")

    if args.concurrency == 1:
        for index, row in enumerate(tqdm(rows, desc="LLM-as-judge")):
            rows[index] = evaluate_row(row, index, args, base_url, api_key)
    else:
        with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
            futures = {
                executor.submit(evaluate_row, row, index, args, base_url, api_key): index
                for index, row in enumerate(rows)
            }
            for future in tqdm(as_completed(futures), total=len(futures), desc="LLM-as-judge"):
                index = futures[future]
                rows[index] = future.result()

    metrics = compute_accuracy(rows)
    metrics.update(
        {
            "model": args.model,
            "method": "llm_as_judge",
            "base_url": base_url,
            "order": args.order,
            "temperature": args.temperature,
            "concurrency": args.concurrency,
            "max_tokens": args.max_tokens,
            "reasoning_effort": args.reasoning_effort,
            "skipped_pairs": sum(1 for row in rows if row.get("skipped")),
        }
    )
    result_path, metrics_path = write_result_bundle(
        rows=rows,
        metrics=metrics,
        output_dir=args.output_dir,
        dataset_path=args.data,
        model_name=args.model,
        method="llm_judge",
    )
    print(f"accuracy={metrics['accuracy']:.4f} ({metrics['correct_pairs']}/{metrics['total_pairs']})")
    print(f"predictions={result_path}")
    print(f"metrics={metrics_path}")


if __name__ == "__main__":
    main()
