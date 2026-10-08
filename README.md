# ScamGraph AI
> **From suspicious messages to complete scam workflows.**
> *Track 2: AI-Driven Multi-Stage Scam Pattern Recognition Platform*

---

## 1. Problem
Digital payment fraud, bank account takeovers, and social engineering attacks across India (UPI, WhatsApp, SMS, NetBanking, electricity notices, job offers, and digital arrests) have evolved beyond crude spam. Fraudsters orchestrate multi-step, multi-channel attack sequences:
$$\text{Unknown Number} \longrightarrow \text{KYC Expiry Threat} \longrightarrow \text{Phishing Link} \longrightarrow \text{Credential Harvest} \longrightarrow \text{OTP / UPI Request}$$
Standard spam filters treat each message as an isolated event, missing the unfolding context, generating alert fatigue, or reacting too late after money has already moved.

---

## 2. Solution: ScamGraph AI
**ScamGraph AI** is a financial-security platform engineered to:
1. **Detect the entire scam workflow** across multiple unfolding events.
2. **Identify unique scam patterns and campaigns** via **Scam DNA** fingerprinting.
3. **Synthesize a calibrated risk index (0–100)** without alert fatigue.
4. **Explain why the interaction is suspicious** in plain, transparent evidence language.
5. **Provide proactive, actionable intervention advice** before money moves.

---

## 3. Key Innovations & Differentiators

| Feature | Legacy Spam Classifiers | ScamGraph AI |
| :--- | :--- | :--- |
| **Perspective** | "Is this text message spam?" | **"What scam workflow is unfolding, what evidence supports that conclusion, and what should the user do next?"** |
| **Workflow Tracking** | Isolated single-event classification | Multi-step state machine tracking 8 canonical scam playbooks |
| **Campaign Attribution** | None (treats every message as new) | **Scam DNA** semantic vectors linking evolving variants into single campaigns |
| **Language Support** | English-centric keyword matching | **MuRIL & Hinglish** multilingual subword and transformer embeddings |
| **Alert Fatigue Control**| Floods users with warnings on every flag | **Adaptive tiering & campaign deduplication** |
| **Explainable AI** | Black-box percentage score | Plain-English evidence points & stage threat prediction |
| **Visual Topology** | Text list | **Interactive Scam Graph** (React Flow) mapping actors, links, and tokens |

---

## 4. System Architecture

```text
                 USER INPUT (SMS / Email / WhatsApp / URL / Transcript)
                                         │
                                         ▼
                                  INPUT PROCESSOR
                                         │
                                         ▼
                            TEXT & ENTITY PREPROCESSING
                   (Preserves URLs, UPI IDs, Phone Numbers, ₹ Amounts)
                                         │
         ┌───────────────────────────────┼──────────────────────────────┐
         ▼                               ▼                              ▼
    NLP MODEL                       RULE ENGINE                    URL ANALYZER
(MuRIL / Multilingual           (Deterministic Evidence         (TLD, Typosquatting,
  Dual Classification)             Weighted Heuristics)           HTTP Protocol)
         │                               │                              │
         └───────────────────────────────┼──────────────────────────────┘
                                         ▼
                                 SIGNAL EXTRACTION
                                         │
                                         ▼
                             SCAM WORKFLOW ENGINE
                   (Playbook Alignment, Stage Progression)
                                         │
                                         ▼
                                 SCAM DNA ENGINE
                   (Semantic Embeddings, Campaign Attribution)
                                         │
                                         ▼
                              COMPOSITE RISK ENGINE
              (Final Score: 0.45*ML + 0.25*Rule + 0.15*URL + 0.15*Workflow)
                                         │
                    ┌────────────────────┴────────────────────┐
                    ▼                                         ▼
            EXPLANATION ENGINE                            SCAM GRAPH
       (Evidence Narrative & Safety)               (React Flow Topology)
                    │                                         │
                    └────────────────────┬────────────────────┘
                                         ▼
                           ADAPTIVE ALERT FATIGUE ENGINE
                       (Zero-Nuisance Tiering & Deduplication)
                                         │
                                         ▼
                                    FINAL RESULT
```

---

## 5. Machine Learning Pipeline

### Dual-Representation Multilingual Architecture
- **Multilingual Transformer (MuRIL)**: Fine-tuning pipeline using `google/muril-base-cased` with a multi-task head (`ml/train_muril.py`) to process Indian English and Romanized Hindi (Hinglish).
- **Subword & Word N-gram Ensemble**: Combines word n-grams (1, 2) and character subword n-grams (2, 5) with sublinear term-frequency scaling and Sigmoid Platt calibrated classification for ultra-fast, calibrated inference (`ml/train_classifier.py`).
- **Classification Heads**:
  - **Head 1**: Binary Classification (`BENIGN` vs `SCAM`).
  - **Head 2**: 13-Class Scam Category Classifier (`KYC`, `UPI`, `OTP`, `PHISHING`, `BANKING`, `JOB`, `LOAN`, `LOTTERY`, `ELECTRICITY`, `INVESTMENT`, `DIGITAL_ARREST`, `IMPERSONATION`, `OTHER`).

---

## 6. Dataset Specifications

### Data Splits & Directory Structure
```text
data/
├── raw/
│   └── scam_dataset_raw.csv      # Complete dataset with authentic patterns
├── processed/
│   └── dataset_stats.json        # Serialized dataset statistics
├── train.csv                     # 70% Stratified Training Split (193 samples)
├── validation.csv                # 15% Stratified Validation Split (41 samples)
└── test.csv                      # 15% Stratified Held-out Test Split (42 samples)
```

### Dataset Statistics (Produced by Training Pipeline)
- **Total Unique Samples**: 276
- **Class Distribution**: 177 Scam (64.1%), 99 Benign (35.9%)
- **Language Distribution**: 222 English (80.4%), 54 Hinglish (19.6%)
- **Fraud Categories Covered**:
  - KYC Fraud, UPI Fraud, OTP Theft, Phishing, Fake Bank Support
  - Job/Task Scam, Loan Scam, Electricity Bill Scam, Lottery/Cashback
  - Digital Arrest Scam, Impersonation, Legitimate Transactions & Alerts

### Dataset Limitations (Documented Transparently)
1. **Regional Variation**: While major Hindi-English transliterations are covered, regional South-Indian Romanized dialects (e.g. Manglish, Tanglish) require supplementary local corpuses.
2. **Synthetic Data Disclosure**: High-volume telemetry figures (e.g., 12,482 aggregate transactions) in the dashboard are generated in Demo Mode for evaluation simulation and are clearly labeled.

---

## 7. Model Evaluation & Benchmark Results

Evaluated on the **held-out 15% stratified test split** (`ml/evaluate.py`):

| Evaluation Metric | Test Score | Operational Significance |
| :--- | :--- | :--- |
| **Fraud Recall** | **100.00%** | **Zero missed scams** (Primary KPI for financial defense) |
| **Precision** | **96.43%** | Very low false positives |
| **F1 Score** | **98.18%** | Robust balance between capture and alert fatigue |
| **ROC-AUC** | **1.0000** | High probability discrimination |
| **Overall Accuracy** | **97.62%** | Correct classifications across test samples |

*Artifacts generated:*
- Confusion Matrix: `ml/reports/confusion_matrix.png`
- Metrics JSON: `ml/reports/metrics.json`
- Markdown Report: `ml/reports/evaluation_report.md`

---

## 8. Multi-Stage Scam Workflow Playbooks

The engine maps event sequences into 8 attack playbooks:

1. **KYC Fraud**: `KYC_WARNING` &rarr; `URGENCY` &rarr; `EXTERNAL_LINK` &rarr; `CREDENTIAL_REQUEST` &rarr; `OTP_REQUEST`
2. **UPI Fraud**: `PAYMENT_LURE` &rarr; `UPI_LINK` &rarr; `URGENCY` &rarr; `PIN_OR_OTP_REQUEST`
3. **Fake Support**: `BANK_SUPPORT_IMPERSONATION` &rarr; `ALERT_DISPUTE` &rarr; `REMOTE_ACCESS_REQUEST` &rarr; `CREDENTIAL_REQUEST`
4. **Job Scam**: `JOB_OFFER` &rarr; `INITIAL_REWARD` &rarr; `REGISTRATION_FEE` &rarr; `PAYMENT_REQUEST`
5. **Electricity Scam**: `DISCONNECTION_THREAT` &rarr; `URGENCY` &rarr; `FAKE_OFFICER_CALL` &rarr; `PAYMENT_REQUEST`
6. **Digital Arrest**: `LAW_ENFORCEMENT_IMPERSONATION` &rarr; `CONTRABAND_ACCUSATION` &rarr; `DIGITAL_ARREST_THREAT` &rarr; `VERIFICATION_ESCROW_TRANSFER`
7. **Loan Scam**: `LOAN_OFFER` &rarr; `INSTANT_APPROVAL` &rarr; `PROCESSING_FEE_REQUEST` &rarr; `PAYMENT_REQUEST`
8. **Lottery Scam**: `LOTTERY_WIN_ANNOUNCEMENT` &rarr; `WHATSAPP_CONTACT` &rarr; `TAX_OR_CLEARANCE_FEE` &rarr; `PAYMENT_REQUEST`

---

## 9. Scam DNA & Emerging Pattern Discovery

### What is Scam DNA?
A unique campaign identifier (e.g. `#UPI-KYC-042`) generated from dense vector embeddings and structural signals. Different wordings of the same campaign map to the same fingerprint:
- *Message A:* "Your SBI KYC will expire today. Update now."
- *Message B:* "Dear customer, your bank KYC is pending. Verify immediately."
Both resolve to `#UPI-KYC-042`.

### Unsupervised Cluster Discovery (DBSCAN)
Analyzed incidents are vectorized and clustered. If a cluster experiences rapid growth:
- `Cluster #UPI-KYC-042`: 117 reports (+64% weekly growth) &rarr; **EMERGING PATTERN DETECTED**
- `Cluster #CYBER-ARREST-104`: 64 reports (+78% weekly growth) &rarr; **EMERGING PATTERN DETECTED**

---

## 10. Alert Fatigue Prevention & Privacy

### Adaptive Alert Tiering
- **LOW (0–29)**: Passive indicator ("Normal communication characteristics").
- **MEDIUM (30–59)**: Advisory warning ("Caution: Suspicious elements present").
- **HIGH (60–79)**: Strong warning ("High risk scam pattern detected").
- **CRITICAL (80–100)**: Immediate blocking intervention ("STOP — Potential financial scam").

### Campaign Deduplication
Repeated messages from known campaigns avoid alert flooding:
> *"🛡️ 118 similar messages detected from active campaign (#UPI-KYC-042)."*

### Privacy by Design
- Automated regex redaction of credit cards, CVVs, passwords, and OTP codes before logging or storage.
- Transient in-memory evaluation without storing unmasked message payloads.
- Cryptographic hashing of sender numbers and reporter identifiers.
- One-click **Purge Incident Logs** action.

---

## 11. Project Structure

```text
scamgraph-ai/
├── backend/
│   ├── api/
│   │   ├── analyze.py
│   │   ├── patterns.py
│   │   ├── dashboard.py
│   │   └── incidents.py
│   ├── database/
│   │   ├── database.py
│   │   └── models.py
│   ├── schemas/
│   │   └── schemas.py
│   ├── services/
│   │   ├── alert_engine.py
│   │   ├── emerging_engine.py
│   │   ├── graph_builder.py
│   │   ├── preprocessing.py
│   │   ├── risk_engine.py
│   │   ├── scam_dna.py
│   │   ├── signal_engine.py
│   │   ├── url_analyzer.py
│   │   └── workflow_engine.py
│   ├── utils/
│   │   └── redactor.py
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AnalyzerView.jsx
│   │   │   ├── DashboardView.jsx
│   │   │   ├── DemoScenario.jsx
│   │   │   ├── EmergingPatternsView.jsx
│   │   │   ├── HeroSection.jsx
│   │   │   ├── Navbar.jsx
│   │   │   ├── PrivacyView.jsx
│   │   │   ├── ResultView.jsx
│   │   │   └── ScamGraphView.jsx
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
├── ml/
│   ├── data_loader.py
│   ├── dataset_generator.py
│   ├── evaluate.py
│   ├── inference.py
│   ├── preprocess.py
│   ├── train_classifier.py
│   ├── train_muril.py
│   ├── reports/
│   │   ├── confusion_matrix.png
│   │   ├── evaluation_report.md
│   │   └── metrics.json
│   └── saved_models/
│       ├── binary_scam_model.joblib
│       ├── category_classifier.joblib
│       └── model_metadata.json
├── data/
│   ├── raw/
│   ├── processed/
│   ├── train.csv
│   ├── validation.csv
│   └── test.csv
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── nginx.conf
├── docs/
│   ├── architecture.md
│   └── api_reference.md
├── notebooks/
│   └── 01_exploratory_analysis.py
├── tests/
│   └── test_api.py
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 12. Local Setup & Execution

### Prerequisites
- Python 3.10+
- Node.js v18+ & npm

### Step 1: Clone & Navigate
```bash
cd scamgraph-ai
```

### Step 2: Backend Setup
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Generate dataset & train models (if re-training)
python ml/dataset_generator.py
python ml/train_classifier.py
python ml/evaluate.py

# Start FastAPI backend
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
API Documentation will be live at `http://127.0.0.1:8000/docs`.

### Step 3: Frontend Setup
In a new terminal:
```bash
cd frontend
npm install
npm run dev
```
Dashboard will be available at `http://localhost:3000`.

### Step 4: Run Test Suite
```bash
python -m pytest tests/test_api.py -v
```

---

## 13. Docker Deployment

Deploy the full stack with Docker Compose:
```bash
docker-compose up --build
```
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`

---

## 14. Demo Instructions (Section 28 Scenario Walkthrough)

Click through the **Guided Scam Evolution Walkthrough** banner at the top of the Analyzer:

1. **Step 1 (Suspicious Threat)**:
   - Input: *"Your bank KYC will expire today. Update immediately."*
   - System registers basic urgency & threat signals.
2. **Step 2 (Phishing URL Introduced)**:
   - Add URL: `http://sbi-kyc-verify.xyz/login`
   - URL analyzer flags brand impersonation and insecure protocol.
3. **Step 3 (Credential Harvest)**:
   - Add: *"Enter PAN and share the OTP to complete verification."*
   - Workflow engine identifies alignment with the KYC Account Takeover playbook.
4. **Step 4 (Workflow Detected & Scam DNA)**:
   - System flags **SCAM WORKFLOW DETECTED**, composite risk escalates to **91/100 (CRITICAL)**, and fingerprinted under `#UPI-KYC-042`.
5. **Step 5 (Emerging Patterns & Scam Graph)**:
   - Click **Interactive Scam Graph** to explore node-link graph visualization.
   - Click **Emerging Patterns** to inspect cluster velocity (+64% growth, 117 reports).
