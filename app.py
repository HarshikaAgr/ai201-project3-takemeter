"""
TakeMeter — Gradio Interface
Stretch Feature: Deployed Interface

Run locally:
    pip install gradio transformers torch
    python app.py

Then open http://localhost:7860 in your browser.

Before running:
    - Replace MODEL_PATH with the path where you saved your fine-tuned model from Colab
    - To save model from Colab: add this at the end of Section 3 in the notebook:
        trainer.save_model("takemeter_model")
        tokenizer.save_pretrained("takemeter_model")
      Then download the takemeter_model/ folder from Colab Files panel.
"""

import gradio as gr
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

# ── Configuration ──────────────────────────────────────────────────────────────

MODEL_PATH = "./takemeter_model"   # path to your saved fine-tuned model folder

LABEL_MAP = {
    0: "analysis",
    1: "hot_take",
    2: "reaction"
}

LABEL_DESCRIPTIONS = {
    "analysis": "This post makes a structured argument with specific, verifiable evidence — stats, historical comparisons, or tactical reasoning.",
    "hot_take": "This post states a bold opinion without meaningful supporting evidence. It asserts rather than argues.",
    "reaction": "This post is an immediate emotional response to a recent event. It expresses a feeling, not a structured claim."
}

LABEL_EMOJIS = {
    "analysis": "📊",
    "hot_take": "🔥",
    "reaction": "😤"
}

# ── Load model ─────────────────────────────────────────────────────────────────

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at '{MODEL_PATH}'.\n"
            "Download your fine-tuned model folder from Colab and place it here.\n"
            "See the comment at the top of this file for instructions."
        )
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    model.eval()
    return tokenizer, model

try:
    tokenizer, model = load_model()
    MODEL_LOADED = True
except Exception as e:
    MODEL_LOADED = False
    LOAD_ERROR = str(e)

# ── Inference ──────────────────────────────────────────────────────────────────

def classify_post(post_text: str):
    """Run the fine-tuned model on a post and return label + confidence."""
    
    if not post_text.strip():
        return "⚠️ Please enter a post.", "", "", {}
    
    if len(post_text.strip()) < 10:
        return "⚠️ Post is too short to classify reliably.", "", "", {}
    
    if not MODEL_LOADED:
        return f"❌ Model not loaded: {LOAD_ERROR}", "", "", {}
    
    # Tokenize and run inference
    inputs = tokenizer(
        post_text,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=True
    )
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=-1).squeeze()
    
    # Get prediction
    predicted_idx = torch.argmax(probs).item()
    predicted_label = LABEL_MAP[predicted_idx]
    confidence = probs[predicted_idx].item()
    
    # Format confidence bar values for all labels
    confidence_dict = {
        f"{LABEL_EMOJIS[LABEL_MAP[i]]} {LABEL_MAP[i]}": float(probs[i])
        for i in range(len(LABEL_MAP))
    }
    
    # Result header
    emoji = LABEL_EMOJIS[predicted_label]
    result_header = f"{emoji} **{predicted_label.upper().replace('_', ' ')}**  ({confidence * 100:.1f}% confidence)"
    
    # Description
    description = LABEL_DESCRIPTIONS[predicted_label]
    
    # Calibration note
    if confidence >= 0.85:
        calibration_note = "High confidence — the model sees clear signals for this label."
    elif confidence >= 0.65:
        calibration_note = "Moderate confidence — this post has some ambiguous features."
    else:
        calibration_note = "Low confidence — this post sits near a label boundary. Consider it borderline."
    
    return result_header, description, calibration_note, confidence_dict


# ── Example posts ──────────────────────────────────────────────────────────────

EXAMPLES = [
    ["Nikola Jokic's assist-to-turnover ratio this season is the highest ever recorded for a center. His passing isn't just impressive for the position — it's historically unprecedented by any positional standard."],
    ["LeBron is the most overrated player in NBA history. His ring chasing and superteam building completely disqualify him from the GOAT conversation."],
    ["I literally cannot breathe. Ja Morant just hit that with 0.4 seconds left. This team is going to give me a heart attack every single night."],
    ["The reason the Lakers' offense collapses in the fourth quarter is their over-reliance on isolation plays — they run isolations on 28% of late-game possessions, highest in the league, producing only 0.87 PPP compared to 1.12 on off-ball sets."],
    ["Steph Curry would never survive in the 90s. Hand-checking alone would've made him a liability on both ends."],
]

# ── Gradio UI ──────────────────────────────────────────────────────────────────

with gr.Blocks(
    title="TakeMeter",
    theme=gr.themes.Base(
        primary_hue="orange",
        secondary_hue="slate",
        neutral_hue="slate",
        font=[gr.themes.GoogleFont("Inter"), "sans-serif"],
    ),
    css="""
    .takemeter-header {
        text-align: center;
        padding: 24px 0 8px 0;
    }
    .takemeter-header h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .takemeter-header p {
        color: #94a3b8;
        font-size: 0.95rem;
    }
    .label-box {
        font-size: 1.1rem;
        font-weight: 600;
        padding: 12px;
        border-radius: 8px;
    }
    .gr-button-primary {
        background: #f97316 !important;
    }
    """
) as demo:

    # Header
    gr.HTML("""
    <div class="takemeter-header">
        <h1>🏀 TakeMeter</h1>
        <p>Fine-tuned NBA discourse classifier &nbsp;·&nbsp; AI201 Project 3 &nbsp;·&nbsp; Harshika Agrawal</p>
    </div>
    """)

    gr.Markdown("""
    Paste any r/nba post or comment below. TakeMeter will classify it as **analysis**, **hot_take**, or **reaction** 
    using a DistilBERT model fine-tuned on 200+ labeled NBA posts.
    """)

    with gr.Row():
        with gr.Column(scale=3):
            post_input = gr.Textbox(
                label="NBA Post or Comment",
                placeholder="Paste an r/nba post here...",
                lines=5,
                max_lines=12,
            )
            classify_btn = gr.Button("Classify This Take →", variant="primary", size="lg")

        with gr.Column(scale=2):
            result_label = gr.Markdown(label="Prediction", elem_classes=["label-box"])
            result_description = gr.Textbox(label="What this label means", lines=2, interactive=False)
            result_calibration = gr.Textbox(label="Confidence note", lines=1, interactive=False)
            confidence_bars = gr.Label(label="Confidence by label", num_top_classes=3)

    gr.Markdown("### Try an example:")
    gr.Examples(
        examples=EXAMPLES,
        inputs=post_input,
        label="Click any example to load it",
    )

    gr.Markdown("""
    ---
    **Label definitions:**
    - 📊 `analysis` — Structured argument with specific, verifiable evidence
    - 🔥 `hot_take` — Bold opinion stated without meaningful supporting evidence  
    - 😤 `reaction` — Immediate emotional response to a specific recent event
    
    *Model: DistilBERT fine-tuned on r/nba posts · Built with 🤗 Transformers + Gradio*
    """)

    # Wire up button
    classify_btn.click(
        fn=classify_post,
        inputs=post_input,
        outputs=[result_label, result_description, result_calibration, confidence_bars],
    )

    # Also classify on Enter
    post_input.submit(
        fn=classify_post,
        inputs=post_input,
        outputs=[result_label, result_description, result_calibration, confidence_bars],
    )

if __name__ == "__main__":
    demo.launch(share=False)
