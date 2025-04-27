#!/bin/bash
# Run the agentic workflow for MQB SAT correctness study
source .venv/bin/activate
python launch_scientist_bfts.py \
  --load_ideas ai_scientist/ideas/mqb_sat_correctness_study.json \
  --load_code \
  --add_dataset_ref \
  --model_writeup o4-mini-2025-04-16 \
  --model_citation gpt-4.1-2025-04-14 \
  --model_review o3-2025-04-16 \
  --model_agg_plots gpt-4.1-2025-04-14 \
  --num_cite_rounds 20
