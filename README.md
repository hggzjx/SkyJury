# SkyJury: Benchmarking User-Conditioned Policy Judgment in Decentralized Moderation

SkyJury is a benchmark for **user-conditioned policy judgment** in decentralized moderation, operationalized through pairwise Bluesky labeler selection. Given a user profile and two plausible Bluesky labelers, a model must decide which selectable governance component is the better match for that user's moderation needs.

The benchmark evaluates two complementary abilities:

- **Verifier accuracy**: whether a model selects the better labeler.
- **Auditor robustness**: whether the model's confidence remains stable under meaning-preserving rubric reformulations.

SkyJury is built from real Bluesky labelers and public rubric definitions. The task is designed to test fine-grained policy judgment rather than handle matching or topical keyword overlap. The current evaluation covers five model families: embedding-based similarity models, dedicated reranking models, discriminative reward models, DPO-style preference models, and LLM-as-a-judge models.

## Framework

![SkyJury pipeline](assets/pipeline.png)


The workflow is:

1. Run a verifier on the original pairwise labeler-selection task.
2. Build rubric reformulations that preserve policy meaning.
3. Re-run the verifier on reformulated variants.
4. Audit confidence shifts with paired statistical tests.

## Benchmark Snapshot

- Benchmark file: `data/skyjury_bench.json`
- Samples: `576`
- High-level categories: `4`
- Fine-grained subsets: `31`

Category counts:

- `safety_moderation`: `128`
- `platform_information_ecology`: `108`
- `interest_community`: `224`
- `identity_trust`: `116`

## Repository Layout

```text
skyjury/
├── README.md
├── assets/
│   └── pipeline.png
├── data/
│   ├── skyjury_bench.json
│   ├── skyjury_bench_summary.md
│   ├── auditor/
│   ├── backups/
│   └── archive_drafts_20260603/
├── labeler_bank/
│   ├── large_labeler_bank.json
│   └── large_labeler_bank_summary.md
├── verifier/
│   ├── run_reward_model.py
│   ├── run_dpo_lm.py
│   ├── run_similarity_model.py
│   ├── run_llm_judge.py
│   ├── run_vllm_judge.py
│   ├── rewardbench_compat.py
│   ├── run_*.sh
│   ├── results/
│   └── logs/
└── auditor/
    ├── build_llm_rubric_perturbations.py
    ├── build_category_subset.py
    ├── audit_cross_candidate_perturbations.py
    ├── audit_stats.py
    ├── run_*.sh
    ├── results/
    ├── archive_legacy_20260603/
    └── archive_legacy_20260604/
```

## Installation

Create a fresh Python environment from the repository root:

```bash
conda create -n skyjury python=3.10 -y
conda activate skyjury
```

Install the core dependencies. For CPU-only exploration, the following is enough:

```bash
pip install torch transformers datasets accelerate huggingface_hub numpy tqdm matplotlib pymupdf sentencepiece protobuf safetensors scikit-learn
```

For GPU evaluation, install the PyTorch build that matches your CUDA runtime first, then install the remaining packages. For example:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cu121
pip install transformers datasets accelerate huggingface_hub numpy tqdm matplotlib pymupdf sentencepiece protobuf safetensors scikit-learn
```

Optional dependencies:

```bash
pip install vllm
```

Use `vllm` only if you plan to run local LLM-as-a-judge inference through `verifier/run_vllm_judge.py`.

## Data Format

The main benchmark file is `data/skyjury_bench.json`. Each item follows an RM-Bench-style pairwise format:

```json
{
  "id": "pref_0001",
  "category": "safety_moderation",
  "subset": "crypto_safety",
  "prompt": "... user profile and behavior context ...",
  "chosen": ["... chosen labeler text ..."],
  "rejected": ["... rejected labeler text ..."]
}
```

The verifier should assign a higher score to `chosen` than to `rejected`.

## Running Verifiers

All examples below assume you are in the repository root:

```bash
cd skyjury
conda activate skyjury
```

### Embedding-Based Similarity Models

Run an embedding model as a user-to-labeler similarity scorer:

```bash
python verifier/run_similarity_model.py \
  --method e5 \
  --model-path /path/to/embedding-model \
  --data data/skyjury_bench.json \
  --output-dir verifier/results/similarity_models/example_embedding \
  --batch-size 32 \
  --max-length 512 \
  --device cuda
```

For BGE-M3, Qwen3-Embedding-8B, or KaLM-Gemma3-12B, pass the local model path with `--model-path`. Lexical baselines are also available through `--method tfidf` and `--method bm25`.

### Dedicated Reranking Models

Run a reranker as a user--candidate relevance scorer:

```bash
python verifier/run_similarity_model.py \
  --method reranker \
  --model-path /path/to/reranker-model \
  --data data/skyjury_bench.json \
  --output-dir verifier/results/reranker_models/example_reranker \
  --batch-size 8 \
  --reranker-max-length 2048 \
  --device cuda \
  --trust-remote-code
```

The reranker path can point to BGE-reranker-v2-m3, Qwen3-Reranker-8B, or Jina-reranker-v3. Internally, these runs are written with the same prediction schema as the other verifier families, so they can be passed directly to the auditor.

### Discriminative Reward Models

Run one reward model with an explicit model path:

```bash
python verifier/run_reward_model.py \
  --model /path/to/reward-model \
  --data data/skyjury_bench.json \
  --output-dir verifier/results/reward_models/example_model \
  --batch-size 4 \
  --max-length 2048 \
  --device cuda \
  --torch-dtype auto \
  --device-map auto
```

The output directory will contain prediction and metric JSON files.

### DPO / Causal-LM Scoring

Run a DPO-style or instruction-tuned causal LM as a scorer:

```bash
python verifier/run_dpo_lm.py \
  --model /path/to/dpo-or-instruction-model \
  --ref-model "" \
  --data data/skyjury_bench.json \
  --output-dir verifier/results/dpo_models/example_model \
  --batch-size 1 \
  --max-length 2048 \
  --device cuda
```

The empty `--ref-model ""` makes the example reference-free and avoids relying on any machine-specific default path. If you have a reference model, pass it with `--ref-model /path/to/reference-model`.

### LLM-as-a-Judge via API

`verifier/run_llm_judge.py` uses an OpenAI-compatible chat-completions endpoint. Set credentials through environment variables:

```bash
export OPENAI_API_KEY_CONF="your_api_key"
export OPENAI_BASE_URL_CONF="https://your-openai-compatible-endpoint/v1/"
```

Then run:

```bash
python verifier/run_llm_judge.py \
  --model gpt-5-ca \
  --data data/skyjury_bench.json \
  --order bidirectional \
  --temperature 0 \
  --concurrency 4 \
  --output-dir verifier/results/generative_rm/gpt-5-ca
```

Use `--dry-run --limit 1` to inspect the prompt without sending API requests:

```bash
python verifier/run_llm_judge.py \
  --data data/skyjury_bench.json \
  --dry-run \
  --limit 1
```

### Local LLM-as-a-Judge

For local generation, use either:

```bash
python verifier/run_local_llm_judge.py \
  --model-path /path/to/local-chat-model \
  --data data/skyjury_bench.json \
  --order bidirectional \
  --output-dir verifier/results/local_llm_judge/example_model
```

or, if `vllm` is installed:

```bash
python verifier/run_vllm_judge.py \
  --model-path /path/to/local-chat-model \
  --data data/skyjury_bench.json \
  --order bidirectional \
  --output-dir verifier/results/vllm_judge/example_model
```

## Running the Auditor

The auditor measures whether verifier confidence changes under rubric reformulations.

### Build Reformulated Datasets

Create length- and language-based rubric reformulations:

```bash
export OPENAI_API_KEY_CONF="your_api_key"
export OPENAI_BASE_URL_CONF="https://your-openai-compatible-endpoint/v1/"
```

```bash
python auditor/build_llm_rubric_perturbations.py \
  --data data/skyjury_bench.json \
  --output-dir data/auditor \
  --prefix skyjury_bench \
  --model deepseek-v4-flash \
  --concurrency 8
```

This writes:

```text
data/auditor/skyjury_bench_base.json
data/auditor/skyjury_bench_rubric_length.json
data/auditor/skyjury_bench_rubric_language.json
data/auditor/skyjury_bench_rubric_perturbation_manifest.json
```

### Build the Category-Balanced Auditor Subset

```bash
python auditor/build_category_subset.py \
  --data-dir data/auditor \
  --output-dir data/auditor/category50 \
  --prefix skyjury_bench \
  --per-category 50 \
  --seed 13
```

This creates a 200-sample auditor subset with 50 examples per high-level category.

### Run Perturbed Verifier Predictions

For example, run an LLM-as-a-judge model on the perturbation datasets:

```bash
python verifier/run_llm_judge.py \
  --model gpt-5-ca \
  --data data/auditor/category50/skyjury_bench_base.json \
  --order bidirectional \
  --temperature 0 \
  --output-dir auditor/results/llm_judge_category50_audit/llm_judge_predictions/gpt-5-ca/base

python verifier/run_llm_judge.py \
  --model gpt-5-ca \
  --data data/auditor/category50/skyjury_bench_rubric_length.json \
  --order bidirectional \
  --temperature 0 \
  --output-dir auditor/results/llm_judge_category50_audit/llm_judge_predictions/gpt-5-ca/length

python verifier/run_llm_judge.py \
  --model gpt-5-ca \
  --data data/auditor/category50/skyjury_bench_rubric_language.json \
  --order bidirectional \
  --temperature 0 \
  --output-dir auditor/results/llm_judge_category50_audit/llm_judge_predictions/gpt-5-ca/language
```

The same pattern applies to embedding, reranking, RM, and DPO scorers: run the verifier on the base, length, and language datasets, then pass the resulting prediction files to the auditor. For embedding and reranking runs, use `--method similarity` when generating auditor reports, because their prediction files share the similarity-style score schema.

### Generate a Robustness Report

```bash
python auditor/audit_cross_candidate_perturbations.py \
  --method llm_judge \
  --original auditor/results/llm_judge_category50_audit/llm_judge_predictions/gpt-5-ca/base/PREDICTIONS.json \
  --perturbed length=auditor/results/llm_judge_category50_audit/llm_judge_predictions/gpt-5-ca/length/PREDICTIONS.json \
  --perturbed language=auditor/results/llm_judge_category50_audit/llm_judge_predictions/gpt-5-ca/language/PREDICTIONS.json \
  --output-dir auditor/results/llm_judge_category50_audit/reports/gpt-5-ca \
  --report-name llm_judge_cross_candidate_rubric_robustness \
  --allow-subset
```

Replace `PREDICTIONS.json` with the concrete `*_predictions.json` file produced by the verifier run.

The bundled `run_*.sh` scripts in `verifier/` and `auditor/` are batch-experiment wrappers for the local experiment setup. They are useful templates, but for a new machine you should check their model paths and output roots before running them directly.

## Outputs

Verifier outputs are written as:

- `*_predictions.json`
- `*_metrics.json`

Auditor reports summarize:

- original vs reformulated confidence shifts
- paired sign-flip permutation tests
- Benjamini-Hochberg-corrected significance markers
- overall and category-wise robustness patterns


## Main Experimental Results

The table below summarizes the main overall results used in the paper. `Acc` is verifier accuracy. Auditor columns report standardized confidence-drop effect sizes; positive values mean the perturbation lowered confidence in the originally chosen labeler. Statistical significance is shown with `*`, `**`, and `***`.

| Family | Model | Acc | len/both | len/cho | len/rej | lang/both | lang/cho | lang/rej |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Embedding | BGE-M3 | 0.519 | -0.0002 | 0.2364*** | -0.2429 | 0.1521* | 1.5004*** | -1.5565 |
| Embedding | Qwen3-Embedding-8B | 0.601 | -0.0195 | -0.3605 | 0.4031*** | -0.0361 | 0.0036 | -0.0595 |
| Embedding | KaLM-Gemma3-12B | 0.634 | 0.0689 | 0.8313*** | -0.8074 | -0.0989 | 1.9013*** | -1.5814 |
| Reranker | BGE-reranker-v2-m3 | 0.457 | -0.0131 | -0.6123 | 0.6187*** | 0.1386 | 0.2356*** | -0.0308 |
| Reranker | Qwen3-Reranker-8B | 0.410 | -0.1228 | 0.2965*** | -0.3208 | -0.1836 | 0.1790** | -0.2062 |
| Reranker | Jina-reranker-v3 | 0.564 | 0.2900*** | 1.6951*** | -1.3224 | 0.0989 | 0.7156*** | -0.4321 |
| RM | ArmoRM-Llama3-8B | 0.632 | 0.0784 | -0.0482 | 0.1129 | 0.0939 | 0.1406** | 0.0033 |
| RM | GRM-Llama3.1-8B | 0.564 | -0.1801 | -0.7727 | 0.6951*** | -0.1414 | 0.3901*** | -0.4353 |
| RM | Skywork-Gemma-2-27B | 0.688 | 0.0710 | -0.1546 | 0.2731*** | 0.1196 | 0.2716*** | -0.1410 |
| RM | Skywork-Llama-3.1-8B | 0.675 | -0.0115 | 0.0243 | 0.0487 | 0.0588 | 0.3997*** | -0.2711 |
| RM | Eurus-RM-7B | 0.524 | -0.1374 | -0.7715 | 0.6700*** | -0.0483 | -0.1914 | 0.1416 |
| DPO | Tulu-2-DPO-13B | 0.509 | -0.0568 | -0.5872 | 0.6180*** | 0.0406 | -0.0277 | 0.1768** |
| DPO | SOLAR-10.7B-Instruct | 0.523 | -0.1439 | -0.8524 | 0.8229*** | -0.0668 | -0.3708 | 0.4280*** |
| Judge | Qwen3-8B | 0.595 | 0.1056 | 0.1017 | 0.1017 | -0.0804 | -0.0819 | -0.0819 |
| Judge | DeepSeek-V4-Pro | 0.632 | -0.0326 | -0.0374 | -0.0374 | -0.0238 | -0.0287 | -0.0287 |
| Judge | MiniMax-M2.7 | 0.644 | -0.0479 | -0.0561 | -0.0561 | -0.0308 | -0.0376 | -0.0376 |
| Judge | Qwen3.5-Plus | **0.731** | 0.0432 | 0.0386 | 0.0386 | 0.0726 | 0.0664 | 0.0664 |
| Judge | GPT-5 | 0.691 | 0.2439*** | 0.2394*** | 0.2394*** | 0.0741 | 0.0699 | 0.0699 |
