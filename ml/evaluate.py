"""
ScamGraph AI - Model Evaluation Pipeline
Evaluates the trained models on the held-out test split (15%).
Produces:
- ml/reports/metrics.json
- ml/reports/confusion_matrix.png
- ml/reports/evaluation_report.md
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

from data_loader import load_splits
from preprocess import normalize_text

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "ml", "saved_models")
REPORTS_DIR = os.path.join(BASE_DIR, "ml", "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def evaluate():
    print("--- Evaluating Models on Held-Out Test Set (15%) ---")
    train_df, val_df, test_df = load_splits()

    binary_model_path = os.path.join(SAVED_MODELS_DIR, "binary_scam_model.joblib")
    category_model_path = os.path.join(SAVED_MODELS_DIR, "category_classifier.joblib")

    if not os.path.exists(binary_model_path) or not os.path.exists(category_model_path):
        raise FileNotFoundError("Models not found. Run train_classifier.py first.")

    binary_pipeline = joblib.load(binary_model_path)
    category_pipeline = joblib.load(category_model_path)

    # 1. Binary Evaluation
    X_test = [normalize_text(t) for t in test_df["text"]]
    y_test_binary = (test_df["label"] == "scam").astype(int)

    test_preds_binary = binary_pipeline.predict(X_test)
    test_probs_binary = binary_pipeline.predict_proba(X_test)[:, 1]

    bin_acc = accuracy_score(y_test_binary, test_preds_binary)
    bin_prec = precision_score(y_test_binary, test_preds_binary, zero_division=0)
    bin_rec = recall_score(y_test_binary, test_preds_binary, zero_division=0)
    bin_f1 = f1_score(y_test_binary, test_preds_binary, zero_division=0)
    bin_auc = roc_auc_score(y_test_binary, test_probs_binary)

    cm = confusion_matrix(y_test_binary, test_preds_binary)

    # 2. Category Evaluation
    y_test_category = test_df["scam_type"].astype(str)
    test_preds_category = category_pipeline.predict(X_test)

    cat_acc = accuracy_score(y_test_category, test_preds_category)
    cat_weighted_f1 = f1_score(y_test_category, test_preds_category, average='weighted', zero_division=0)

    # Generate Confusion Matrix Plot
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=['Benign', 'Scam'], yticklabels=['Benign', 'Scam'], ax=ax)
    ax.set_title('Test Set Confusion Matrix (Scam vs Benign)')
    ax.set_ylabel('True Label')
    ax.set_xlabel('Predicted Label')
    plt.tight_layout()
    cm_plot_path = os.path.join(REPORTS_DIR, "confusion_matrix.png")
    fig.savefig(cm_plot_path, dpi=200)
    plt.close()
    print(f"Saved confusion matrix plot: {cm_plot_path}")

    # Save metrics.json
    metrics_data = {
        "dataset_split": {
            "test_samples": len(test_df),
            "scam_samples": int(sum(y_test_binary == 1)),
            "benign_samples": int(sum(y_test_binary == 0))
        },
        "binary_classification": {
            "accuracy": float(round(bin_acc, 4)),
            "precision": float(round(bin_prec, 4)),
            "recall": float(round(bin_rec, 4)),
            "f1_score": float(round(bin_f1, 4)),
            "roc_auc": float(round(bin_auc, 4)),
            "confusion_matrix": {
                "true_negative": int(cm[0][0]),
                "false_positive": int(cm[0][1]),
                "false_negative": int(cm[1][0]),
                "true_positive": int(cm[1][1])
            }
        },
        "category_classification": {
            "accuracy": float(round(cat_acc, 4)),
            "weighted_f1": float(round(cat_weighted_f1, 4))
        }
    }

    metrics_json_path = os.path.join(REPORTS_DIR, "metrics.json")
    with open(metrics_json_path, "w") as f:
        json.dump(metrics_data, f, indent=2)
    print(f"Saved metrics JSON: {metrics_json_path}")

    # Generate evaluation_report.md
    report_md = f"""# ScamGraph AI - Model Evaluation Report

## Test Dataset Summary
- **Evaluation Set**: Held-out Test Split (15% of dataset)
- **Total Test Samples**: {len(test_df)}
- **Scam Samples**: {sum(y_test_binary == 1)}
- **Benign Samples**: {sum(y_test_binary == 0)}
- **Multilingual Support**: Indian English, Romanized Hindi (Hinglish)

## Binary Classification (BENIGN vs SCAM)
| Metric | Score | Description |
| :--- | :--- | :--- |
| **Recall (Fraud Detection)** | **{bin_rec * 100:.2f}%** | Fraud capture rate (minimizing false negatives) |
| **F1 Score** | **{bin_f1 * 100:.2f}%** | Harmonic balance between precision and recall |
| **Precision** | **{bin_prec * 100:.2f}%** | Accuracy of scam flags (minimizing false alarms) |
| **ROC-AUC** | **{bin_auc:.4f}** | Area under the ROC curve for calibrated confidence |
| **Accuracy** | **{bin_acc * 100:.2f}%** | Overall classification correctness |

### Confusion Matrix Breakdown
- **True Positives (Scams correctly flagged)**: {cm[1][1]}
- **True Negatives (Benign correctly allowed)**: {cm[0][0]}
- **False Positives (Benign misclassified as Scam)**: {cm[0][1]}
- **False Negatives (Missed Scams)**: {cm[1][0]}

## Category Classification (13 Categories)
- **Test Accuracy**: {cat_acc * 100:.2f}%
- **Weighted F1 Score**: {cat_weighted_f1 * 100:.2f}%
- **Supported Categories**: KYC, UPI, OTP, PHISHING, BANKING, JOB, LOAN, LOTTERY, ELECTRICITY, INVESTMENT, DIGITAL_ARREST, IMPERSONATION, OTHER

## Pipeline Architecture
- **Features**: Dual-representation FeatureUnion combining Word N-grams (1, 2) and Character Subword N-grams (2, 5) with sublinear TF scaling.
- **Classification Engine**: Calibrated Logistic Regression with Sigmoid Platt Scaling for calibrated risk probabilities.
- **Explainability**: Integrated with Rule-based Signal Engine and Workflow State Transition Engine.
"""

    report_md_path = os.path.join(REPORTS_DIR, "evaluation_report.md")
    with open(report_md_path, "w") as f:
        f.write(report_md)
    print(f"Saved evaluation markdown report: {report_md_path}")

    print("\n--- Evaluation Summary ---")
    print(f"Recall: {bin_rec:.4f} | Precision: {bin_prec:.4f} | F1: {bin_f1:.4f} | ROC-AUC: {bin_auc:.4f}")
    return metrics_data


if __name__ == "__main__":
    evaluate()
