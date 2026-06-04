# SkyJury Preference Verifier

This verifier follows the RM-Bench evaluation idea: given the same user profile prompt, a judge/reward model should assign a higher score to the `chosen` Labeler than to the `rejected` Labeler.

## Data

Default dataset:

```bash
/ssd1/lbh/zjx/skyjury/data/skyjury_bench.json
```

Each row is RM-Bench style:

```json
{
  "id": "pref_0001",
  "subset": "crypto_safety",
  "prompt": "... user profile and behavior context ...",
  "chosen": ["... candidate Labeler text ..."],
  "rejected": ["... candidate Labeler text ..."]
}
```

## Environment

The local `rm_dev` conda environment already contains the core runtime used here:

- `torch`
- `transformers`
- `datasets`
- `accelerate`
- `huggingface_hub`

The SkyJury verifier uses a local RewardBench-compatible adapter in `rewardbench_compat.py`.
It follows RewardBench's model-specific configuration idea, chat-template formatting, reward-output extraction, and DPO policy/reference scoring, but avoids importing the local `RewardAuditor/rewardbench` package directly because that checkout is missing `rewardbench.models` and has incompatible optional dependencies in this environment.

## Model Download

Default baseline models:

- RM: `OpenAssistant/reward-model-deberta-v3-large-v2`
- DPO/LM scorer: `HuggingFaceH4/zephyr-7b-beta`

Download them into `/ssd1/lbh/zjx/models/skyjury_verifier`:

```bash
cd /ssd1/lbh/zjx/skyjury/verifier
source activate rm_dev
export HF_ENDPOINT=https://hf-mirror.com
python download_models.py
```

Or start the mirror download in tmux:

```bash
bash /ssd1/lbh/zjx/skyjury/verifier/start_model_download_tmux.sh
```

## Run RewardBench-Compatible RM

```bash
bash /ssd1/lbh/zjx/skyjury/verifier/run_rm.sh
```

Equivalent explicit command:

```bash
cd /ssd1/lbh/zjx/skyjury/verifier
source activate rm_dev
python run_reward_model.py \
  --model /ssd1/lbh/zjx/models/skyjury_verifier/OpenAssistant_reward-model-deberta-v3-large-v2 \
  --data /ssd1/lbh/zjx/skyjury/data/skyjury_bench.json \
  --batch-size 4 \
  --max-length 2048 \
  --local-files-only
```

## Run DPO / Causal LM Scorer

Reference-free scoring:

```bash
bash /ssd1/lbh/zjx/skyjury/verifier/run_dpo.sh
```

With an optional reference model:

```bash
bash /ssd1/lbh/zjx/skyjury/verifier/run_dpo.sh \
  /path/to/dpo_or_instruction_model \
  /ssd1/lbh/zjx/skyjury/data/skyjury_bench.json \
  /path/to/reference_model
```

The DPO runner scores each candidate with answer-token log probability conditioned on the user profile prompt. `--ref-free-type` supports RewardBench-style `sum`, `avg`, and `norm` reductions. If `--ref-model` is provided, it uses policy-minus-reference log-ratio as the preference score.

## Run Generative Reward Model / LLM-as-Judge

This path evaluates closed-source or API-served generative models as judges. The API must be OpenAI-compatible and expose `/chat/completions`.

Set credentials through environment variables. Do not hard-code API keys in scripts:

```bash
export OPENAI_API_KEY_CONF="..."
export OPENAI_BASE_URL_CONF="https://api.chatanywhere.tech/v1/"
```

Then run:

```bash
bash /ssd1/lbh/zjx/skyjury/verifier/run_llm_judge.sh
```

Equivalent explicit command:

```bash
cd /ssd1/lbh/zjx/skyjury/verifier
source activate rm_dev
python run_llm_judge.py \
  --model gpt-4o-mini \
  --data /ssd1/lbh/zjx/skyjury/data/skyjury_bench.json \
  --order bidirectional \
  --temperature 0 \
  --concurrency 4
```

The judge is asked to output only the final preference decision:

```json
{"winner":"A"}
```

No rationale or explanation is requested.

`--order bidirectional` asks the judge twice for each pair: once with `chosen=A, rejected=B`, and once with the candidates swapped. This reduces candidate-position bias. The script maps judge votes back into:

```text
score_chosen > score_rejected
```

and then computes the same preference accuracy as the RM and DPO runners.

`--concurrency` controls sample-level parallel API calls. The default is `1` for fully serial behavior. Higher values such as `4` or `8` can speed up generative judge evaluation if the API endpoint allows concurrent requests. Each sample still evaluates its own normal/swapped calls in order, so the output JSON format stays the same.

To inspect the exact prompt without calling the API:

```bash
python run_llm_judge.py --dry-run --limit 1
```

## Outputs

Results are written to:

```bash
/ssd1/lbh/zjx/skyjury/verifier/results
```

Each run produces:

- `*_predictions.json`: original rows plus `score_chosen` and `score_rejected`
- `*_metrics.json`: overall accuracy and subset accuracy

The main verifier metric is:

```text
Accuracy = mean(score(chosen) > score(rejected))
```
