## ✅ How to Check Proper Installation (No Conda Required!)

Before running AI Scientist-v2, make sure the following tools and libraries are installed and available in your environment:

### 1. Python Packages (in your venv)
Install with:
```bash
pip install -r requirements.txt
```

### 2. PyTorch, torchvision, torchaudio, CUDA
Check with:
```bash
python -c "import torch; import torchvision; import torchaudio; print('torch:', torch.__version__, 'cuda:', torch.cuda.is_available())"
```
- Output should show versions and `cuda: True` if you have GPU support.

### 3. Poppler (for pdftotext)
Check with:
```bash
which pdftotext
pdftotext -v
```
- Output should show the path and version.
- If missing, install with:
  `sudo apt-get install poppler-utils`

### 4. ChkTeX (for LaTeX linting)
Check with:
```bash
which chktex
chktex --version
```
- Output should show the path and version.
- If missing, install with:
  `sudo apt-get install chktex`

---

## 🔍 Quick Dependency Check Script

You can copy and run this script to check all dependencies at once:

```bash
echo "Checking Python packages..."
python -c "import torch; import torchvision; import torchaudio; print('torch:', torch.__version__, 'cuda:', torch.cuda.is_available())" || echo "PyTorch or related packages missing!"

echo "Checking pdftotext (poppler)..."
which pdftotext && pdftotext -v || echo "pdftotext (poppler-utils) missing!"

echo "Checking chktex..."
which chktex && chktex --version || echo "chktex missing!"
```

---

## Example Output (Sollte so aussehen):

```
torch: 2.2.0 cuda: True
/usr/bin/pdftotext
pdftotext version 22.02.0
/usr/bin/chktex
ChkTeX v1.7.6 - Copyright 1995-96 Jens T. Berger Thielemann.
```

---

**Führe die Checks jetzt durch:**

```bash
python -c "import torch; import torchvision; import torchaudio; print('torch:', torch.__version__, 'cuda:', torch.cuda.is_available())"
which pdftotext && pdftotext -v
which chktex && chktex --version
```

---

If any check fails, install the missing tool as shown above.

---

## 🚀 Model Selection Recommendations (2025)

### Choosing the Best LLMs for Agentic Science

Based on the latest benchmarks and pricing, we recommend the following models for different steps in your agentic workflow:

| Step            | Model Name                   | Provider   | Notes                            |
|-----------------|-----------------------------|------------|----------------------------------|
| Writeup         | o4-mini-2025-04-16          | OpenAI     | Fast, affordable, good reasoning |
| Citation        | gpt-4.1-2025-04-14          | OpenAI     | Flagship, high accuracy          |
| Review          | o3-2025-04-16               | OpenAI     | High capacity, robust            |
| Plots           | gpt-4.1-2025-04-14          | OpenAI     | Flagship, complex tasks          |
| Any step        | claude-3-7-sonnet-20250219  | Anthropic  | Latest Claude Sonnet, strong reasoning |

- **Mix and match** these models for maximum performance and cost efficiency.
- Specify the model for each step using the `--model_writeup`, `--model_citation`, `--model_review`, and `--model_agg_plots` flags.
- Example launch command:

```bash
python launch_scientist_bfts.py \
  --load_ideas ai_scientist/ideas/deep_understanding_mqb_idea_1.json \
  --load_code \
  --add_dataset_ref \
  --model_writeup o4-mini-2025-04-16 \
  --model_citation gpt-4.1-2025-04-14 \
  --model_review o3-2025-04-16 \
  --model_agg_plots gpt-4.1-2025-04-14 \
  --num_cite_rounds 20
```

- To use Anthropic for any step, simply use `claude-3-7-sonnet-20250219` as the model name for that step.

### Model Power & Pricing (2025)

| Model Name                  | Input $/1M | Output $/1M | Context Window | Max Output | Notes                      |
|-----------------------------|------------|-------------|---------------|------------|----------------------------|
| o4-mini-2025-04-16          | $1.10      | $4.40       | 200,000       | 100,000    | Fast, affordable           |
| gpt-4.1-2025-04-14          | $2.00      | $8.00       | 1,047,576     | 32,768     | Flagship, complex tasks    |
| o3-2025-04-16               | $10.00     | $40.00      | 200,000       | 100,000    | Most powerful, robust      |
| claude-3-7-sonnet-20250219  | (see Anthropic pricing) | (see Anthropic pricing) | Large         | Large      | Latest Claude Sonnet       |

- See [OpenAI Pricing](https://openai.com/pricing) and [Anthropic Pricing](https://docs.anthropic.com/claude/docs/pricing) for up-to-date details.

---

**For best results, always use the latest model names and adjust for your workflow needs!**

---

## 💡 How Many Ideas Will Be Generated?

By default, the ideation script (`perform_ideation_temp_free.py`) generates **one** idea per run. If you want more ideas in your JSON file, use the `--max-num-generations` flag. For example:

```bash
python ai_scientist/perform_ideation_temp_free.py \
  --workshop-file ai_scientist/ideas/deep_understanding_mqb.md \
  --max-num-generations 5
```

This will generate 5 distinct proposals and store them in the same JSON file. Adjust the number as needed for your workflow.

If you run with the default settings (no `--max-num-generations`), only 1 idea will be generated and stored.

---
=======
The AI Scientist-v2 completes experiments with a success rate that depends on the chosen foundation model, and the complexity of the idea. Higher success rates are generally observed when using powerful models like Claude 3.5 Sonnet for the experimentation phase.

**What is the estimated cost per experiment?**

Using Claude 3.5 Sonnet for the experimentation phase typically costs around $15–$20 per run. The subsequent writing phase adds approximately $5 when using the default models specified in the example command. Using GPT-4o for `model_citation` is recommended as it can help reduce writing costs.

**How do I run The AI Scientist-v2 for different subject fields?**

You can add a new JSON file to the `ai_scientist/ideas/` directory. For reference, take a look at the example: `ai_scientist/ideas/i_cant_believe_its_not_better.json`.

**What should I do if I have problems accessing the Semantic Scholar API?**

The Semantic Scholar API is used to assess the novelty of generated ideas and to gather citations during the paper write-up phase. If you don't have an API key, encounter rate limits, you may be able to skip these phases.

**I encountered a "CUDA Out of Memory" error. What can I do?**

This error typically occurs when the AI Scientist-v2 attempts to load or run a model that requires more GPU memory than available on your system. To resolve this, you can try updating your idea's JSON file (`ai_scientist/ideas/your_idea.json`) to suggest using a smaller model for the experiments or analysis.

## Acknowledgement

The tree search component implemented within the `ai_scientist` directory is built on top of the [AIDE](https://github.com/WecoAI/aideml) project. We thank the AIDE developers for their valuable contributions and for making their work publicly available.


## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=SakanaAI/AI-Scientist-v2&type=Date)](https://star-history.com/#SakanaAI/AI-Scientist-v2&Date)

