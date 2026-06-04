source activate rm_dev
cd /ssd1/lbh/zjx/skyjury/auditor

python build_llm_rubric_perturbations.py \
  --data /ssd1/lbh/zjx/skyjury/data/skyjury_bench.json \
  --output-dir /ssd1/lbh/zjx/skyjury/data/auditor \
  --prefix skyjury_bench \
  --model deepseek-v4-flash \
  --concurrency 48 \
  --request-jitter 8 \
  --timeout 180 \
  --retries 8 \
  --max-tokens 12000