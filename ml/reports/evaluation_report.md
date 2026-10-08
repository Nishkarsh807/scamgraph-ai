# ScamGraph AI - Model Evaluation Report

## Test Dataset Summary
- **Evaluation Set**: Held-out Test Split (15% of dataset)
- **Total Test Samples**: 42
- **Scam Samples**: 27
- **Benign Samples**: 15
- **Multilingual Support**: Indian English, Romanized Hindi (Hinglish)

## Binary Classification (BENIGN vs SCAM)
| Metric | Score | Description |
| :--- | :--- | :--- |
| **Recall (Fraud Detection)** | **100.00%** | Fraud capture rate (minimizing false negatives) |
| **F1 Score** | **98.18%** | Harmonic balance between precision and recall |
| **Precision** | **96.43%** | Accuracy of scam flags (minimizing false alarms) |
| **ROC-AUC** | **1.0000** | Area under the ROC curve for calibrated confidence |
| **Accuracy** | **97.62%** | Overall classification correctness |

### Confusion Matrix Breakdown
- **True Positives (Scams correctly flagged)**: 27
- **True Negatives (Benign correctly allowed)**: 14
- **False Positives (Benign misclassified as Scam)**: 1
- **False Negatives (Missed Scams)**: 0

## Category Classification (13 Categories)
- **Test Accuracy**: 90.48%
- **Weighted F1 Score**: 90.65%
- **Supported Categories**: KYC, UPI, OTP, PHISHING, BANKING, JOB, LOAN, LOTTERY, ELECTRICITY, INVESTMENT, DIGITAL_ARREST, IMPERSONATION, OTHER

## Pipeline Architecture
- **Features**: Dual-representation FeatureUnion combining Word N-grams (1, 2) and Character Subword N-grams (2, 5) with sublinear TF scaling.
- **Classification Engine**: Calibrated Logistic Regression with Sigmoid Platt Scaling for calibrated risk probabilities.
- **Explainability**: Integrated with Rule-based Signal Engine and Workflow State Transition Engine.
