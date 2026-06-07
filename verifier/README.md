# SkyJury Verifier

This directory contains verifier runners for SkyJury:

- `run_reward_model.py`: discriminative reward-model scoring
- `run_dpo_lm.py`: DPO / causal-LM scoring
- `run_llm_judge.py`: OpenAI-compatible API judge
- `run_local_llm_judge.py`: local Hugging Face causal-LM judge
- `run_vllm_judge.py`: local vLLM judge

For installation, data format, and portable run examples, see the top-level documentation:

- [../README.md](../README.md)

The shell scripts in this directory are batch-experiment wrappers. They may contain local model paths from the original experiment environment, so use the Python commands in the top-level README as the portable starting point.
