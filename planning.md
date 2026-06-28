# TakeMeter — Planning Document
**Author:** Harshika Agrawal | UCID: ha542 | AI201 Project 3
**Community:** r/nba (NBA Subreddit)
**Written:** Before data collection (Milestone 2)

---

## 1. Community

I chose **r/nba**, the official NBA subreddit with over 7 million members. This community is a strong fit for a classification task for three reasons:

First, the discourse is genuinely varied in structure and quality — you'll find a 300-word breakdown of a player's shot mechanics sitting next to "THIS GUY CANNOT SHOOT" in the same comment section. That range makes the classification task meaningful rather than trivial.

Second, r/nba has a strong internal culture around discourse quality. Regular members openly distinguish between "actual analysis" and "hot takes," and the community frequently calls out opinions that lack evidence. The labels I'm using aren't invented by me — they map directly onto how people in this community already talk about post quality.

Third, the community is text-heavy and public. Posts and top-level comments are accessible without authentication, span a wide range of topics (player comparisons, game reactions, trade rumors, tactical debates), and generate enough volume that collecting 200 labeled examples manually is realistic in 1–2 hours.

---

## 2. Label Taxonomy

I am using **3 labels**: `analysis`, `hot_take`, and `reaction`.

### `analysis`
**Definition:** A post that makes a structured argument about basketball, supported by specific and verifiable evidence — statistics, historical comparisons, tactical observations, or film-based reasoning — where the evidence would still support the claim even if the opinion framing were removed.

**Example 1:**
> "People forget that Nikola Jokic's assist-to-turnover ratio this season (5.8) is the highest ever recorded for a center. His passing isn't just impressive for the position — it's historically unprecedented by any positional standard."

*Why this is `analysis`:* Cites a specific, verifiable stat (5.8 AST/TO ratio for a center), makes a historical comparison, and the claim stands even without the "people forget" framing.

**Example 2:**
> "The reason the Lakers' offense collapses in the fourth quarter is their over-reliance on isolation plays — per Cleaning the Glass, they run isolations on 28% of late-game possessions, second-highest in the league, and those possessions produce only 0.87 PPP compared to their off-ball sets at 1.12."

*Why this is `analysis`:* Uses play-type data with a source, presents a cause-effect argument, and compares two specific numbers.

---

### `hot_take`
**Definition:** A bold, confident opinion stated without meaningful supporting evidence — the post asserts a strong claim but does not argue for it with verifiable data or structured reasoning; any evidence cited is vague, cherry-picked, or decorative.

**Example 1:**
> "LeBron is the most overrated player in NBA history. His ring chasing and superteam building completely disqualify him from the GOAT conversation."

*Why this is `hot_take`:* Strong claim, zero verifiable evidence, relies entirely on assertion and loaded framing ("ring chasing," "superteam building" used as conclusions rather than supported claims).

**Example 2:**
> "Steph Curry would never survive in the 90s. That era would have destroyed him — hand-checking alone would've made him a liability on both ends."

*Why this is `hot_take`:* Counterfactual claim stated as certainty, no evidence for how hand-checking would specifically affect Curry's game, no acknowledgment of his size/athleticism/shooting range.

---

### `reaction`
**Definition:** An immediate emotional response to a specific, recent event (a game, a trade, an injury, a play) with little to no argument — the post expresses a feeling in the moment rather than making or defending a claim.

**Example 1:**
> "I literally cannot breathe. Ja Morant just hit that with 0.4 seconds left. This team is going to give me a heart attack every single night."

*Why this is `reaction`:* Triggered by a specific recent play, expresses pure emotional response, no argument or claim being made.

**Example 2:**
> "The refs stole this game. That's all I have to say. Absolute joke of a call with 2 minutes left."

*Why this is `reaction`:* Immediate frustration at a specific event, no evidence or structured reasoning, purely expressive.

---

## 3. Hard Edge Cases

### Primary edge case: The stat-dressed hot take

**The post type:** A post that includes one or two specific stats but uses them to dress up a fundamentally assertive opinion rather than to construct a real argument.

**Example:**
> "LeBron is overrated — his playoff win rate against top-seeded opponents is below .500. He's a regular-season king."

This post cites a real, verifiable stat. But is it `analysis` or `hot_take`?

**My decision rule:** If the evidence presented would support the full claim on its own — meaning you could remove the opinion framing and the evidence still makes the case — label it `analysis`. If the stat is selected to support a predetermined conclusion, is cherry-picked for effect, or doesn't actually prove what the post claims, label it `hot_take`.

In the example above: "below .500 against top seeds" is a real stat, but it's cherry-picked (ignores lower seeds, Finals appearances, team context) and used to make a sweeping character claim ("regular-season king"). The evidence doesn't support the conclusion on its own. → **`hot_take`**

**Tiebreaker:** Ask "could a statistician reasonably disagree with the evidence selection?" If yes, it's a hot take dressed up as analysis.

### Secondary edge case: The passionate reaction with a claim embedded

**The post type:** An emotional reaction post that also contains a clear opinion or claim.

**Example:**
> "I'm so sick of this team. They've lost 6 of their last 8 and Darvin Ham STILL won't adjust the rotation. Fire him."

This reacts emotionally to recent games but also makes a claim (Ham won't adjust rotations, he should be fired).

**My decision rule:** If the primary purpose of the post is expressing a feeling about a recent event, and the claim is subordinate to the emotional expression, label it `reaction`. If the claim is the main point and the emotion is framing for it, label it `hot_take`.

The "fire him" post is primarily venting frustration. → **`reaction`**

### Documented difficult annotation cases (updated during Milestone 3)

*(To be filled in as I annotate — at least 3 cases required)*

| # | Post text (excerpt) | Possible labels | Decision | Reasoning |
|---|---|---|---|---|
| 1 | TBD | TBD | TBD | TBD |
| 2 | TBD | TBD | TBD | TBD |
| 3 | TBD | TBD | TBD | TBD |

---

## 4. Data Collection Plan

**Source:** r/nba on Reddit — top posts and comments from the past 12 months, accessed manually through the web interface (old.reddit.com for easier browsing). I will also use subreddit search to target specific label types when one label is underrepresented.

**Target distribution:**
| Label | Target count | Minimum acceptable |
|---|---|---|
| `analysis` | 70 | 60 |
| `hot_take` | 70 | 60 |
| `reaction` | 70 | 60 |
| **Total** | **210** | **200** |

**Collection strategy by label:**
- `analysis`: Search for posts with long comment threads, "X breakdown," "film study," player comparison threads. Top comments in game threads that include stats are also good sources.
- `hot_take`: Search for "unpopular opinion," "hot take," player GOAT debates, trade rumors. "Change my mind" style posts.
- `reaction`: Game threads (post-game discussion threads), injury reaction posts, trade deadline reactions. These are the easiest to find.

**If a label is underrepresented after 150 examples:**
I will use Reddit search within r/nba with targeted keywords specific to that label (e.g., for `analysis`: "per game stats," "shooting percentage," "historical"). I will not manufacture examples or reuse posts — all examples must be real r/nba posts or comments.

**What I will NOT collect:**
- Posts under 10 words (too short to classify reliably)
- Posts that are primarily links, images, or videos with no substantive text
- Memes, jokes, or clearly off-topic posts
- Duplicate posts from the same thread

**CSV format:** `text`, `label`, `notes` (third column for edge case documentation)

---

## 5. Evaluation Metrics

I will use the following metrics, and here is why each one is necessary:

**Overall accuracy** is a starting point but not enough on its own. With 3 balanced classes, a random guesser would hit ~33% accuracy — so accuracy only becomes meaningful when read alongside per-class performance.

**Per-class F1 score** is my primary metric because this task has no "safe" direction to be wrong. Missing a `reaction` (calling it `analysis`) is equally bad as missing an `analysis` (calling it `reaction`) — neither type of error is more costly. F1 is the harmonic mean of precision and recall, and gives a single number that penalizes both over-prediction and under-prediction for each label.

**Precision and recall per class** in addition to F1, because they tell you the *direction* of failure:
- High precision, low recall on `analysis` = the model is too conservative about calling something analysis (misses many real analysis posts)
- High recall, low precision on `reaction` = the model over-calls reaction (cries wolf)

**Confusion matrix** tells me exactly which label pairs are being confused and in which direction. This is essential for the error pattern analysis stretch feature — I need to know if the model specifically confuses `hot_take` → `analysis` (the stat-dressed take problem) or `reaction` → `hot_take` (the emotional claim problem).

**Cohen's kappa** for the inter-annotator reliability stretch feature — this corrects for agreement by chance, which simple percentage agreement does not. For a 3-class task, expected agreement by chance is ~33%, so raw agreement is misleading without kappa.

**Confidence calibration** (stretch): I will bin predictions by confidence score (e.g., 50–60%, 60–70%, etc.) and report actual accuracy within each bin. A well-calibrated model should have actual accuracy match its confidence — 70% confident predictions should be right ~70% of the time.

---

## 6. Definition of Success

**Minimum bar for "good enough to deploy":**
- Fine-tuned model overall accuracy ≥ 65% (meaningfully above the 33% random baseline)
- All three per-class F1 scores ≥ 0.55 (no label completely learned or completely missed)
- Fine-tuned model beats Groq zero-shot baseline on overall accuracy

**Target for a strong project:**
- Fine-tuned model overall accuracy ≥ 75%
- All three per-class F1 scores ≥ 0.70
- Cohen's kappa with second annotator ≥ 0.60 (substantial agreement)

**Why these thresholds:**
A classifier deployed in a real community tool (e.g., a browser extension that flags takes on r/nba) would need to be right more often than a general-purpose LLM with no fine-tuning — otherwise, why fine-tune? The 65% floor ensures fine-tuning added real value. The 0.55 per-class floor ensures the model isn't just predicting one class constantly.

I can objectively determine at the end whether I hit these thresholds — they are specific numbers, not subjective judgments.

---

## 7. AI Tool Plan

### Label stress-testing (before annotation)
I will give Claude my three label definitions and the two edge case descriptions, and ask it to generate 10 posts that sit at the `analysis`/`hot_take` boundary — specifically stat-dressed hot takes at varying levels of evidence quality. If I can't cleanly classify the generated posts using my decision rules, I will tighten the rules before annotating 200 examples. I will document what posts it generated and what I changed.

### Annotation assistance (during Milestone 3)
I plan to use Claude to pre-label batches of 20 posts at a time. I will provide:
- My full label definitions and decision rules from this document
- The unlabeled posts
- An instruction to output only `analysis`, `hot_take`, or `reaction` — one per line

I will then review every pre-assigned label myself and correct any I disagree with. I will track which examples were pre-labeled in a fourth column (`prelabeled_by_ai`) in my CSV, and disclose this in my README AI usage section. I will not accept the pre-label without reading the post myself.

### Failure analysis (after Milestone 5)
After fine-tuning, I will paste all misclassified test examples into Claude and ask it to: (1) identify any common patterns in the failures, (2) note whether wrong predictions cluster around a specific label pair, and (3) flag any posts where my own labeling may have been inconsistent. I will then re-read those examples myself to verify Claude's pattern claims before including them in my evaluation report. If Claude's pattern claim doesn't hold up on re-reading, I'll say so in the report.

---

## 8. Stretch Features Plan

*(To be updated before starting each stretch feature)*

### Inter-annotator reliability
I will ask a classmate to independently label 30–40 of my examples using only the label definitions from Section 2 of this document (not my decision rules). I will compute Cohen's kappa and analyze the disagreements — specifically whether they cluster around the `analysis`/`hot_take` boundary (the hardest distinction) or are spread randomly across all boundaries.

### Confidence calibration
After fine-tuning, I will extract the softmax probability for the predicted class for every test example. I will bin predictions into 10-percentage-point intervals (50–60%, 60–70%, etc.) and compute actual accuracy within each bin. I will plot or table these results and report whether the model is overconfident, underconfident, or well-calibrated.

### Error pattern analysis
I will go beyond listing 3 individual wrong predictions. I will systematically categorize all wrong predictions by: (1) which label pair was confused, (2) post length (short < 50 words, medium 50–150, long > 150), and (3) presence of any numbers or statistics. I will identify at least one systematic pattern (not just individual cases) and explain what it reveals about the model's learned decision boundary.

### Deployed Gradio interface
I will build a Gradio app that: (1) accepts a free-text NBA post, (2) runs it through the fine-tuned DistilBERT model, and (3) returns the predicted label, confidence score, and a brief explanation of what that label means. The interface code will be committed to the repo and documented in the README with instructions for running locally.

---

*Last updated: Milestone 2 (before data collection)*
*Next update: Before starting stretch features (Milestone 5/6)*
