# ml/finetune_intent.py

import json
import torch
import numpy as np
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
)
from peft import get_peft_model, LoraConfig, TaskType
from sklearn.metrics import f1_score, classification_report
from sklearn.model_selection import train_test_split

# ── Intent Dataset ───────────────────────────────────────────────────────────────
# Labels: 0 = targeting_query, 1 = performance_query, 2 = audience_query
SAMPLES = [
    ("How do I target users by age and income?", 0),
    ("Set up demographic targeting for my campaign", 0),
    ("Create a lookalike audience from my customer list", 0),
    ("Target users who visited my website last week", 0),
    ("Show ads only to users in New York and California", 0),
    ("How do I retarget abandoned cart users?", 0),
    ("Set up interest-based targeting for sports fans", 0),
    ("Target high-income users aged 25 to 45", 0),
    ("How do I suppress already-converted users?", 0),
    ("Create a behavioral targeting segment", 0),

    ("What is the CTR for my last campaign?", 1),
    ("Show me my ROAS and CPA metrics", 1),
    ("How is my campaign performing this week?", 1),
    ("What is the click-through rate on my ads?", 1),
    ("Compare performance of campaign A and campaign B", 1),
    ("What is my cost per acquisition?", 1),
    ("Which ad creative has the highest conversion rate?", 1),
    ("Show me the ROC curve for my model", 1),
    ("How do I measure campaign success?", 1),
    ("What is my return on ad spend?", 1),

    ("Who is in my target audience?", 2),
    ("Describe the characteristics of my best customers", 2),
    ("What segments exist in my customer base?", 2),
    ("Show me my audience breakdown by age group", 2),
    ("What is the size of my retargeting audience?", 2),
    ("Who are my highest-value customers?", 2),
    ("What are the demographics of my email list?", 2),
    ("Describe my lookalike audience profile", 2),
    ("What types of users engage with my ads?", 2),
    ("Show me my customer segmentation report", 2),
]

LABEL_NAMES = ["targeting_query", "performance_query", "audience_query"]
MODEL_NAME = "distilbert-base-uncased"

# ── Prepare Data ─────────────────────────────────────────────────────────────────
texts = [s[0] for s in SAMPLES]
labels = [s[1] for s in SAMPLES]

train_texts, test_texts, train_labels, test_labels = train_test_split(
    texts, labels, test_size=0.3, random_state=42, stratify=labels
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def tokenize(batch):
    return tokenizer(batch["text"], padding="max_length", truncation=True, max_length=64)

train_dataset = Dataset.from_dict({"text": train_texts, "label": train_labels})
test_dataset  = Dataset.from_dict({"text": test_texts,  "label": test_labels})
train_dataset = train_dataset.map(tokenize, batched=True)
test_dataset  = test_dataset.map(tokenize, batched=True)
train_dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])
test_dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])

# ── Zero-Shot Baseline ────────────────────────────────────────────────────────────
print("\n── Zero-Shot Baseline (no fine-tuning) ──")
base_model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME, num_labels=3, ignore_mismatched_sizes=True
)
base_model.eval()

def get_predictions(model, dataset):
    preds = []
    with torch.no_grad():
        for i in range(len(dataset)):
            item = dataset[i]
            input_ids = item["input_ids"].unsqueeze(0)
            attention_mask = item["attention_mask"].unsqueeze(0)
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            pred = torch.argmax(outputs.logits, dim=1).item()
            preds.append(pred)
    return preds

zero_shot_preds = get_predictions(base_model, test_dataset)
zero_shot_f1 = f1_score(test_labels, zero_shot_preds, average="weighted", zero_division=0)
print(f"Zero-Shot F1 (weighted): {zero_shot_f1:.4f}")
print(classification_report(test_labels, zero_shot_preds, target_names=LABEL_NAMES, zero_division=0))

# ── LoRA Fine-Tuning ─────────────────────────────────────────────────────────────
print("\n── Fine-Tuning with LoRA/PEFT ──")
ft_model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME, num_labels=3, ignore_mismatched_sizes=True
)

lora_config = LoraConfig(
    task_type=TaskType.SEQ_CLS,
    r=8,
    lora_alpha=16,
    lora_dropout=0.1,
    target_modules=["q_lin", "v_lin"],
)
ft_model = get_peft_model(ft_model, lora_config)
ft_model.print_trainable_parameters()

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    f1 = f1_score(labels, preds, average="weighted", zero_division=0)
    return {"f1": f1}

training_args = TrainingArguments(
    output_dir="./lora_intent_model",
    num_train_epochs=5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    eval_strategy="epoch",
    save_strategy="no",
    logging_steps=5,
    learning_rate=2e-4,
    weight_decay=0.01,
    report_to="none",
)

trainer = Trainer(
    model=ft_model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    compute_metrics=compute_metrics,
)

trainer.train()

# ── Fine-Tuned Evaluation ─────────────────────────────────────────────────────────
print("\n── Fine-Tuned Model Results ──")
ft_model.eval()
ft_preds = get_predictions(ft_model, test_dataset)
ft_f1 = f1_score(test_labels, ft_preds, average="weighted", zero_division=0)
print(f"Fine-Tuned F1 (weighted): {ft_f1:.4f}")
print(classification_report(test_labels, ft_preds, target_names=LABEL_NAMES, zero_division=0))

# ── Save Benchmark Results ────────────────────────────────────────────────────────
benchmark = {
    "model_base": MODEL_NAME,
    "peft_method": "LoRA",
    "lora_r": 8,
    "lora_alpha": 16,
    "zero_shot_f1": round(zero_shot_f1, 4),
    "finetuned_f1": round(ft_f1, 4),
    "improvement": round(ft_f1 - zero_shot_f1, 4),
    "label_names": LABEL_NAMES,
}

with open("finetune_benchmark.json", "w") as f:
    json.dump(benchmark, f, indent=2)

print("\n" + "=" * 50)
print(f"✅ Benchmark Complete!")
print(f"   Zero-Shot F1:    {zero_shot_f1:.4f}")
print(f"   Fine-Tuned F1:   {ft_f1:.4f}")
print(f"   Improvement:     +{ft_f1 - zero_shot_f1:.4f}")
print(f"   Saved to:        finetune_benchmark.json")
print("=" * 50)