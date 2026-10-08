"""
ScamGraph AI - Production ML Training Pipeline
Trains:
1. Binary Classifier: BENIGN vs SCAM with probability calibration
2. Multi-class Scam Category Classifier: KYC, UPI, OTP, PHISHING, BANKING, JOB, LOAN, LOTTERY, ELECTRICITY, INVESTMENT, DIGITAL_ARREST, IMPERSONATION, OTHER
Evaluates on validation split, logs parameters, and saves model artifacts.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score

from data_loader import load_splits
from preprocess import normalize_text

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "ml", "saved_models")
os.makedirs(SAVED_MODELS_DIR, exist_ok=True)


def build_feature_pipeline():
    """
    Combines word n-grams (1, 2) and character subword n-grams (2, 5)
    to effectively capture Hinglish morphology, typo variations, and brand impersonations.
    """
    word_vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=4000,
        sublinear_tf=True
    )
    char_vectorizer = TfidfVectorizer(
        ngram_range=(2, 5),
        analyzer='char',
        max_features=6000,
        sublinear_tf=True
    )
    features = FeatureUnion([
        ("word", word_vectorizer),
        ("char", char_vectorizer)
    ])
    return features


def train_binary_model(train_df: pd.DataFrame, val_df: pd.DataFrame):
    """
    Train binary model (BENIGN vs SCAM) with probability calibration
    """
    print("--- Training Binary Model (BENIGN vs SCAM) ---")
    X_train = [normalize_text(t) for t in train_df["text"]]
    y_train = (train_df["label"] == "scam").astype(int)

    X_val = [normalize_text(t) for t in val_df["text"]]
    y_val = (val_df["label"] == "scam").astype(int)

    # Use class_weight='balanced' to prioritize recall on fraud
    base_clf = LogisticRegression(C=2.5, class_weight='balanced', max_iter=1000, random_state=42)
    pipeline = Pipeline([
        ("features", build_feature_pipeline()),
        ("classifier", CalibratedClassifierCV(estimator=base_clf, method='sigmoid', cv=3))
    ])

    pipeline.fit(X_train, y_train)

    val_preds = pipeline.predict(X_val)
    val_probs = pipeline.predict_proba(X_val)[:, 1]

    acc = accuracy_score(y_val, val_preds)
    rec = recall_score(y_val, val_preds)
    prec = precision_score(y_val, val_preds)
    f1 = f1_score(y_val, val_preds)

    print(f"Validation Binary Metrics: Accuracy={acc:.4f}, Precision={prec:.4f}, Recall={rec:.4f}, F1={f1:.4f}")
    print(classification_report(y_val, val_preds, target_names=["BENIGN", "SCAM"]))

    # Save artifact
    binary_path = os.path.join(SAVED_MODELS_DIR, "binary_scam_model.joblib")
    joblib.dump(pipeline, binary_path)
    print(f"Saved binary model to: {binary_path}")

    return pipeline, {
        "val_accuracy": float(acc),
        "val_precision": float(prec),
        "val_recall": float(rec),
        "val_f1": float(f1)
    }


def train_category_model(train_df: pd.DataFrame, val_df: pd.DataFrame):
    """
    Train multi-class category model: KYC, UPI, OTP, PHISHING, BANKING, etc.
    """
    print("\n--- Training Category Model (13 Classes) ---")
    # Train primarily on scam examples or all examples with defined category
    train_cat_df = train_df.copy()
    val_cat_df = val_df.copy()

    X_train = [normalize_text(t) for t in train_cat_df["text"]]
    y_train = train_cat_df["scam_type"].astype(str)

    X_val = [normalize_text(t) for t in val_cat_df["text"]]
    y_val = val_cat_df["scam_type"].astype(str)

    category_clf = LogisticRegression(C=2.0, class_weight='balanced', max_iter=1000, random_state=42)
    cat_pipeline = Pipeline([
        ("features", build_feature_pipeline()),
        ("classifier", category_clf)
    ])

    cat_pipeline.fit(X_train, y_train)

    val_preds = cat_pipeline.predict(X_val)
    classes = list(cat_pipeline.classes_)

    acc = accuracy_score(y_val, val_preds)
    f1 = f1_score(y_val, val_preds, average='weighted', zero_division=0)
    print(f"Validation Category Metrics: Accuracy={acc:.4f}, Weighted F1={f1:.4f}")

    cat_path = os.path.join(SAVED_MODELS_DIR, "category_classifier.joblib")
    joblib.dump(cat_pipeline, cat_path)
    print(f"Saved category model to: {cat_path}")

    return cat_pipeline, {
        "val_accuracy": float(acc),
        "val_weighted_f1": float(f1),
        "classes": [str(c) for c in classes]
    }


def main():
    train_df, val_df, test_df = load_splits()
    print(f"Loaded splits: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}")

    bin_pipeline, bin_metrics = train_binary_model(train_df, val_df)
    cat_pipeline, cat_metrics = train_category_model(train_df, val_df)

    metadata = {
        "model_architecture": "TF-IDF (Word 1-2 + Char 2-5) + Calibrated Logistic Regression",
        "multilingual_support": "Indian English & Hinglish",
        "dataset_split": "70% Train, 15% Validation, 15% Test",
        "binary_metrics": bin_metrics,
        "category_metrics": cat_metrics,
        "supported_categories": [
            "kyc", "upi", "otp", "phishing", "banking", "job", "loan",
            "lottery", "electricity", "investment", "digital_arrest", "impersonation", "other"
        ]
    }

    meta_path = os.path.join(SAVED_MODELS_DIR, "model_metadata.json")
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"\nSaved metadata to: {meta_path}")


if __name__ == "__main__":
    main()
