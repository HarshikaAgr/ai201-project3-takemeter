# TakeMeter 🏀

**AI201 Project 3 — Fine-Tuned Text Classifier**
**Author:** Harshika Agrawal | UCID: ha542
**Community:** r/nba (NBA Subreddit)

TakeMeter is a fine-tuned text classifier that evaluates discourse quality in NBA Reddit posts. Given any r/nba post or comment, the model classifies it as `analysis`, `hot_take`, or `reaction` — distinctions that matter deeply to people who actually participate in the community.

---

## Community Choice

I chose **r/nba**, the official NBA subreddit with over 7 million members. This community is an ideal fit for a classification task because the discourse varies enormously in quality and structure — a 300-word breakdown of shot mechanics and "THIS GUY CANNOT SHOOT" can appear in the same comment section. More importantly, r/nba has a strong internal culture around discourse quality: members openly distinguish "actual analysis" from "hot takes," and frequently call out opinions that lack evidence. The three labels I'm using aren't invented — they map directly onto how people in this community already talk about post quality.

---

## Label Taxonomy

### `analysis`
A post that makes a structured argument supported by specific, verifiable evidence — statistics, historical comparisons, or tactical observations. The evidence would still support the claim even if the opinion framing were removed.

**Example 1:**
> "Nikola Jokic's assist-to-turnover ratio this season (5.8) is the highest ever recorded for a center. His passing isn't just impressive for the position — it's historically unprecedented by any positional standard."

**Example 2:**
> "The reason the Lakers' offense collapses in the fourth quarter is their over-reliance on isolation plays — per Cleaning the Glass, they run isolations on 28% of late-game possessions, second-highest in the league, producing only 0.87 PPP compared to their off-ball sets at 1.12."

---

### `hot_take`
A bold, confident opinion stated without meaningful supporting evidence. The post asserts a strong claim but does not argue for it with verifiable data or structured reasoning. Any evidence cited is vague, cherry-picked, or decorative.

**Example 1:**
> "LeBron is the most overrated player in NBA history. His ring chasing and superteam building completely disqualify him from the GOAT conversation."

**Example 2:**
> "Steph Curry would never survive in the 90s. Hand-checking alone would've made him a liability on both ends."

---

### `reaction`
An immediate emotional response to a specific recent event — a game, trade, injury, or play. The post expresses a feeling in the moment rather than making or defending a claim.

**Example 1:**
> "I literally cannot breathe. Ja Morant just hit that with 0.4 seconds left. This team is going to give me a heart attack every single night."

**Example 2:**
> "The refs stole this game. That's all I have to say. Absolute joke of a call with 2 minutes left."

---

## Data Collection

**Source:** r/nba on Reddit — top posts and comments from the past 12 months, accessed manually through old.reddit.com.

**Labeling process:** Each post was read in full and assigned exactly one label using the definitions above. A decision rule was applied for ambiguous cases (see `planning.md`). Approximately one-third of examples were pre-labeled using Claude with my label definitions, then reviewed and corrected by hand before finalizing.

**Label distribution:**

| Label | Count |
|---|---|
| `analysis` | — |
| `hot_take` | — |
| `reaction` | — |
| **Total** | — |

*(To be filled in after data collection)*

**Difficult-to-label examples:**

| # | Post excerpt | Possible labels | Decision | Reasoning |
|---|---|---|---|---|
| 1 | — | — | — | — |
| 2 | — | — | — | — |
| 3 | — | — | — | — |

*(To be filled in during annotation)*

---

## Fine-Tuning Approach

**Base model:** `distilbert-base-uncased` (HuggingFace)

**Training setup:**
- Framework: HuggingFace `transformers` + `Trainer` API
- Runtime: Google Colab T4 GPU
- Epochs: 3
- Learning rate: 2e-5
- Batch size: 16 (train), 32 (eval)
- Train/val/test split: 70% / 15% / 15% (stratified)

**Key hyperparameter decision:** *(To be filled in after training — note what you changed and why, or confirm defaults were kept)*

---

## Baseline

**Model:** `llama-3.3-70b-versatile` via Groq API (zero-shot — no task-specific training)

**Prompt approach:** The system prompt provided my three label definitions verbatim from `planning.md`, one example post per label, and an explicit instruction to output only the label name. Temperature was set to 0 for deterministic output.

**How results were collected:** The baseline was run on the same locked test set as the fine-tuned model, before fine-tuning began (Milestone 4). Results were parsed automatically; responses not matching a valid label were flagged as unparseable.

---

## Evaluation Report

### Overall Accuracy

| Model | Accuracy |
|---|---|
| Zero-shot baseline (Groq) | — |
| Fine-tuned DistilBERT | — |
| Improvement | — |

*(To be filled in after Colab Section 6)*

### Per-Class Metrics

**Fine-tuned model:**

| Label | Precision | Recall | F1 |
|---|---|---|---|
| `analysis` | — | — | — |
| `hot_take` | — | — | — |
| `reaction` | — | — | — |

**Baseline (Groq):**

| Label | Precision | Recall | F1 |
|---|---|---|---|
| `analysis` | — | — | — |
| `hot_take` | — | — | — |
| `reaction` | — | — | — |

*(To be filled in after Colab)*

### Confusion Matrix (Fine-Tuned Model)

*(To be filled in after Colab Section 4 — write as markdown table)*

| | Predicted: analysis | Predicted: hot_take | Predicted: reaction |
|---|---|---|---|
| **True: analysis** | — | — | — |
| **True: hot_take** | — | — | — |
| **True: reaction** | — | — | — |

### Wrong Predictions — Error Analysis

*(To be filled in after Colab Section 4 — analyze 3 specific wrong predictions)*

**Wrong prediction #1:**
- **Post:** —
- **True label:** —
- **Predicted:** —
- **Analysis:** —

**Wrong prediction #2:**
- **Post:** —
- **True label:** —
- **Predicted:** —
- **Analysis:** —

**Wrong prediction #3:**
- **Post:** —
- **True label:** —
- **Predicted:** —
- **Analysis:** —

### Sample Classifications

*(To be filled in after fine-tuning)*

| Post excerpt | Predicted label | Confidence | Notes |
|---|---|---|---|
| — | — | — | — |

---

## Reflection: What the Model Learned vs. What I Intended

*(To be filled in after evaluation)*

---

## Stretch Features

### Inter-Annotator Reliability
*(To be filled in)*

### Confidence Calibration
*(To be filled in)*

### Error Pattern Analysis
*(To be filled in)*

### Deployed Interface
The Gradio interface is in `app.py`. To run it locally:

```bash
pip install gradio transformers torch
python app.py
```

Before running, download your fine-tuned model from Colab:
1. At the end of Section 3 in the notebook, add:
   ```python
   trainer.save_model("takemeter_model")
   tokenizer.save_pretrained("takemeter_model")
   ```
2. Download the `takemeter_model/` folder from the Colab Files panel
3. Place it in the same directory as `app.py`

Then open `http://localhost:7860` in your browser.

---

## Spec Reflection

*(To be filled in after project completion)*

**One way the spec helped:** —

**One way my implementation diverged:** —

---

## AI Usage

*(To be filled in — at least 2 specific instances)*

**Instance 1:**
- **What I asked:** —
- **What it produced:** —
- **What I changed/overrode:** —

**Instance 2:**
- **What I asked:** —
- **What it produced:** —
- **What I changed/overrode:** —

**Annotation disclosure:** *(Disclose if you used an LLM to pre-label any examples)*

---

## Repository Structure

```
ai201-project3-takemeter/
├── planning.md                 # Design thinking: labels, edge cases, metrics, AI tool plan
├── README.md                   # This file — final evaluation report
├── app.py                      # Gradio interface (stretch feature)
├── nba_dataset.csv             # Labeled dataset (200+ examples)
├── evaluation_results.json     # Model comparison output from Colab
└── confusion_matrix.png        # Confusion matrix from Colab Section 4
```
