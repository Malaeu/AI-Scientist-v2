## ✅ How to Check Proper Installation (No Conda Required!)

Before running AI Scientist-v2, make sure the following tools and libraries are installed and available in your environment:


----


<p align="center">
  📚 <a href="https://pub.sakana.ai/ai-scientist-v2/paper">[Paper]</a> |
  📝 <a href="https://sakana.ai/ai-scientist-first-publication/"> [Blog Post]</a> |
  📂 <a href="https://github.com/SakanaAI/AI-Scientist-ICLR2025-Workshop-Experiment"> [ICLR2025 Workshop Experiment]</a>
</p>

Fully autonomous scientific research systems are becoming increasingly capable, with AI playing a pivotal role in transforming how scientific discoveries are made.
We are excited to introduce The AI Scientist-v2, a generalized end-to-end agentic system that has generated the first workshop paper written entirely by AI and accepted through peer review.

This system autonomously generates hypotheses, runs experiments, analyzes data, and writes scientific manuscripts. Unlike [its predecessor (AI Scientist-v1)](https://github.com/SakanaAI/AI-Scientist), the AI Scientist-v2 removes reliance on human-authored templates, generalizes across Machine Learning (ML) domains, and employs a progressive agentic tree search, guided by an experiment manager agent.

> **Note:**
> The AI Scientist-v2 doesn’t necessarily produce better papers than v1, especially when a strong starting template is available. v1 follows well-defined templates, leading to high success rates, while v2 takes a broader, more exploratory approach with lower success rates. v1 works best for tasks with clear objectives and a solid foundation, whereas v2 is designed for open-ended scientific exploration.

> **Caution!**
> This codebase will execute Large Language Model (LLM)-written code. There are various risks and challenges associated with this autonomy, including the potential use of dangerous packages, uncontrolled web access, and the possibility of spawning unintended processes. Ensure that you run this within a controlled sandbox environment (e.g., a Docker container). Use at your own discretion.

## Table of Contents

1.  [Requirements](#requirements)
    *   [Installation](#installation)
    *   [Supported Models and API Keys](#supported-models-and-api-keys)
2.  [Generate Research Ideas](#generate-research-ideas)
3.  [Run AI Scientist-v2 Paper Generation Experiments](#run-ai-scientist-v2-paper-generation-experiments)
4.  [Citing The AI Scientist-v2](#citing-the-ai-scientist-v2)
5.  [Frequently Asked Questions](#frequently-asked-questions)
6.  [Acknowledgement](#acknowledgement)

## Requirements

This code is designed to run on Linux with NVIDIA GPUs using CUDA and PyTorch.

### Installation

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


----


#### Semantic Scholar API (Literature Search)

Our code can optionally use a Semantic Scholar API Key (`S2_API_KEY`) for higher throughput during literature search [if you have one](https://www.semanticscholar.org/product/api). This is used during both the ideation and paper writing stages. The system should work without it, though you might encounter rate limits or reduced novelty checking during ideation. If you experience issues with Semantic Scholar, you can skip the citation phase during paper generation.

#### Setting API Keys

Ensure you provide the necessary API keys as environment variables for the models you intend to use. For example:
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


----


## Generate Research Ideas

Before running the full AI Scientist-v2 experiment pipeline, you first use the `ai_scientist/perform_ideation_temp_free.py` script to generate potential research ideas. This script uses an LLM to brainstorm and refine ideas based on a high-level topic description you provide, interacting with tools like Semantic Scholar to check for novelty.

1.  **Prepare a Topic Description:** Create a Markdown file (e.g., `my_research_topic.md`) describing the research area or theme you want the AI to explore. This file should contain sections like `Title`, `Keywords`, `TL;DR`, and `Abstract` to define the scope of the research. Refer to the example file `ai_scientist/ideas/i_cant_believe_its_not_better.md` for the expected structure and content format. Place your file in a location accessible by the script (e.g., the `ai_scientist/ideas/` directory).

2.  **Run the Ideation Script:** Execute the script from the main project directory, pointing it to your topic description file and specifying the desired LLM.

    ```bash
    python ai_scientist/perform_ideation_temp_free.py \
     --workshop-file "ai_scientist/ideas/my_research_topic.md" \
     --model gpt-4o-2024-05-13 \
     --max-num-generations 20 \
     --num-reflections 5
    ```
    *   `--workshop-file`: Path to your topic description Markdown file.
    *   `--model`: The LLM to use for generating ideas (ensure you have the corresponding API key set).
    *   `--max-num-generations`: How many distinct research ideas to attempt generating.
    *   `--num-reflections`: How many refinement steps the LLM should perform for each idea.

3.  **Output:** The script will generate a JSON file named after your input Markdown file (e.g., `ai_scientist/ideas/my_research_topic.json`). This file will contain a list of structured research ideas, including hypotheses, proposed experiments, and related work analysis.

4.  **Proceed to Experiments:** Once you have the generated JSON file containing research ideas, you can proceed to the next section to run the experiments.

This ideation step guides the AI Scientist towards specific areas of interest and produces concrete research directions to be tested in the main experimental pipeline.

## Run AI Scientist-v2 Paper Generation Experiments

Using the JSON file generated in the previous ideation step, you can now launch the main AI Scientist-v2 pipeline. This involves running experiments via agentic tree search, analyzing results, and generating a paper draft.

Specify the models used for the write-up and review phases via command-line arguments.
The configuration for the best-first tree search (BFTS) is located in `bfts_config.yaml`. Adjust parameters in this file as needed.

```
torch: 2.2.0 cuda: True
/usr/bin/pdftotext
pdftotext version 22.02.0
/usr/bin/chktex
ChkTeX v1.7.6 - Copyright 1995-96 Jens T. Berger Thielemann.
```

---


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


----


Example command to run AI-Scientist-v2 using a generated idea file (e.g., `my_research_topic.json`). Please review `bfts_config.yaml` for detailed tree search parameters (the default config includes `claude-3-5-sonnet` for experiments).


----


Example command to run AI-Scientist-v2 using a generated idea file (e.g., `my_research_topic.json`). Please review `bfts_config.yaml` for detailed tree search parameters (the default config includes `claude-3-5-sonnet` for experiments). Do not set `load_code` if you do not want to initialize experimentation with a code snippet.


```bash
python launch_scientist_bfts.py \
 --load_ideas "ai_scientist/ideas/my_research_topic.json" \
 --load_code \
 --add_dataset_ref \
 --model_writeup o1-preview-2024-09-12 \
 --model_citation gpt-4o-2024-11-20 \
 --model_review gpt-4o-2024-11-20 \
 --model_agg_plots o3-mini-2025-01-31 \
 --num_cite_rounds 20
```

Once the initial experimental stage is complete, you will find a timestamped log folder inside the `experiments/` directory. Navigate to `experiments/"timestamp_ideaname"/logs/0-run/` within that folder to find the tree visualization file `unified_tree_viz.html`.

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


----


The AI Scientist-v2 completes experiments with a success rate that depends on the chosen foundation model, and the complexity of the idea. Higher success rates are generally observed when using powerful models like Claude 3.5 Sonnet for the experimentation phase.

**What is the estimated cost per experiment?**

The ideation step cost depends on the LLM used and the number of generations/reflections, but is generally low (a few dollars). For the main experiment pipeline, using Claude 3.5 Sonnet for the experimentation phase typically costs around $15–$20 per run. The subsequent writing phase adds approximately $5 when using the default models specified in the example command. Using GPT-4o for `model_citation` is recommended as it can help reduce writing costs.

**How do I run The AI Scientist-v2 for different subject fields?**

First, perform the [Generate Research Ideas](#generate-research-ideas) step. Create a new Markdown file describing your desired subject field or topic, following the structure of the example `ai_scientist/ideas/i_cant_believe_its_not_better.md`. Run the `perform_ideation_temp_free.py` script with this file to generate a corresponding JSON idea file. Then, proceed to the [Run AI Scientist-v2 Paper Generation Experiments](#run-ai-scientist-v2-paper-generation-experiments) step, using this JSON file with the `launch_scientist_bfts.py` script via the `--load_ideas` argument.

**What should I do if I have problems accessing the Semantic Scholar API?**

The Semantic Scholar API is used to assess the novelty of generated ideas and to gather citations during the paper write-up phase. If you don't have an API key, encounter rate limits, you may be able to skip these phases.

**I encountered a "CUDA Out of Memory" error. What can I do?**

This error typically occurs when the AI Scientist-v2 attempts to load or run a model that requires more GPU memory than available on your system. To resolve this, you can try updating your ideation prompt file (`ai_scientist/ideas/my_research_topic.md`) to suggest using smaller models for the experiments.

## Acknowledgement

The tree search component implemented within the `ai_scientist` directory is built on top of the [AIDE](https://github.com/WecoAI/aideml) project. We thank the AIDE developers for their valuable contributions and for making their work publicly available.


## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=SakanaAI/AI-Scientist-v2&type=Date)](https://star-history.com/#SakanaAI/AI-Scientist-v2&Date)

