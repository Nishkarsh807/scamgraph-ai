"""
ScamGraph AI - Multilingual Transformer (MuRIL) Training Pipeline
Fine-tunes Google's MuRIL (Multilingual Representations for Indian Languages)
for Indian English & Hinglish scam detection with dual-task heads:
Head 1: Binary Classification (BENIGN vs SCAM)
Head 2: Multi-class Category Classification (13 Scam Types)
"""

import os
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModel, AdamW, get_linear_schedule_with_warmup
import pandas as pd
import numpy as np
from typing import Dict, Any

from data_loader import load_splits
from preprocess import normalize_text

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "ml", "saved_models")
os.makedirs(SAVED_MODELS_DIR, exist_ok=True)

MODEL_NAME = "google/muril-base-cased"
FALLBACK_MODEL = "bert-base-multilingual-cased"

CATEGORY_MAPPING = {
    "kyc": 0, "upi": 1, "otp": 2, "phishing": 3, "banking": 4, "job": 5,
    "loan": 6, "lottery": 7, "electricity": 8, "investment": 9,
    "digital_arrest": 10, "impersonation": 11, "other": 12
}
REV_CATEGORY_MAPPING = {v: k for k, v in CATEGORY_MAPPING.items()}


class ScamDataset(Dataset):
    def __init__(self, texts, labels, categories, tokenizer, max_len=128):
        self.texts = [normalize_text(t) for t in texts]
        self.labels = labels
        self.categories = [CATEGORY_MAPPING.get(str(c).lower(), 12) for c in categories]
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=self.max_len,
            return_tensors="pt"
        )
        return {
            "input_ids": encoding["input_ids"].flatten(),
            "attention_mask": encoding["attention_mask"].flatten(),
            "binary_label": torch.tensor(self.labels[idx], dtype=torch.long),
            "category_label": torch.tensor(self.categories[idx], dtype=torch.long)
        }


class MuRILScamClassifier(nn.Module):
    """
    Multi-task architecture on top of MuRIL:
    Shared multilingual encoder ->
    1) Binary classification head (benign/scam)
    2) Category classification head (13 classes)
    """
    def __init__(self, base_model_name: str = MODEL_NAME, num_categories: int = 13, dropout: float = 0.3):
        super().__init__()
        try:
            self.encoder = AutoModel.from_pretrained(base_model_name)
        except Exception as e:
            print(f"Warning: Could not download {base_model_name} offline. Using {FALLBACK_MODEL} or mock weights: {e}")
            self.encoder = AutoModel.from_pretrained(FALLBACK_MODEL)

        hidden_size = self.encoder.config.hidden_size
        self.dropout = nn.Dropout(dropout)
        self.binary_head = nn.Linear(hidden_size, 2)
        self.category_head = nn.Linear(hidden_size, num_categories)

    def forward(self, input_ids, attention_mask):
        outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        # Use [CLS] token representation or mean pool
        cls_rep = outputs.last_hidden_state[:, 0, :]
        pooled = self.dropout(cls_rep)
        
        binary_logits = self.binary_head(pooled)
        category_logits = self.category_head(pooled)
        return binary_logits, category_logits


def train_muril_pipeline(epochs: int = 3, batch_size: int = 8, lr: float = 2e-5):
    """
    Executes MuRIL fine-tuning pipeline.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device for MuRIL training: {device}")

    train_df, val_df, test_df = load_splits()

    print(f"Loading Tokenizer for {MODEL_NAME}...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    except Exception as e:
        print(f"Falling back to {FALLBACK_MODEL}: {e}")
        tokenizer = AutoTokenizer.from_pretrained(FALLBACK_MODEL)

    train_dataset = ScamDataset(
        train_df["text"].tolist(),
        (train_df["label"] == "scam").astype(int).tolist(),
        train_df["scam_type"].tolist(),
        tokenizer
    )
    val_dataset = ScamDataset(
        val_df["text"].tolist(),
        (val_df["label"] == "scam").astype(int).tolist(),
        val_df["scam_type"].tolist(),
        tokenizer
    )

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)

    model = MuRILScamClassifier(base_model_name=MODEL_NAME).to(device)

    criterion_bin = nn.CrossEntropyLoss(weight=torch.tensor([1.5, 1.0]).to(device))
    criterion_cat = nn.CrossEntropyLoss()
    optimizer = AdamW(model.parameters(), lr=lr)

    print("Beginning MuRIL fine-tuning epochs...")
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for batch in train_loader:
            optimizer.zero_grad()
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            bin_labels = batch["binary_label"].to(device)
            cat_labels = batch["category_label"].to(device)

            bin_logits, cat_logits = model(input_ids, attention_mask)
            loss_bin = criterion_bin(bin_logits, bin_labels)
            loss_cat = criterion_cat(cat_logits, cat_labels)
            loss = loss_bin + 0.5 * loss_cat

            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"Epoch {epoch+1}/{epochs} - Avg Loss: {total_loss / len(train_loader):.4f}")

    # Save fine-tuned checkpoint
    save_path = os.path.join(SAVED_MODELS_DIR, "muril_scam_model.pt")
    torch.save(model.state_dict(), save_path)
    print(f"Saved MuRIL model weights to: {save_path}")


if __name__ == "__main__":
    train_muril_pipeline(epochs=1)
