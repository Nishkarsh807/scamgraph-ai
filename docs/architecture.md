# ScamGraph AI — System Architecture Specification

## 1. High-Level System Architecture

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

## 2. Core Architectural Pillars

### Pillar 1: Multilingual Machine Learning
- **Transformer Encoder**: Supports Google's MuRIL (*Multilingual Representations for Indian Languages*) and character-level n-gram subword representations to reliably identify mixed Hinglish and Indian-English fraud phrasing without breaking on phonetic slang or spelling obfuscations.
- **Dual Classification Heads**:
  - Head 1: Binary classification (BENIGN vs SCAM) with sigmoid Platt scaling calibration.
  - Head 2: 13-class taxonomy classifier (KYC, UPI, OTP, Phishing, Fake Support, Job Scam, Loan Scam, Lottery, Electricity, Investment, Digital Arrest, Impersonation, Other).

### Pillar 2: Scam Workflow Intelligence
Unlike standard spam filters that evaluate inputs as isolated points in time, ScamGraph AI tracks interactions against canonical attack playbooks:
1. **KYC Fraud**: `KYC_WARNING` &rarr; `URGENCY` &rarr; `EXTERNAL_LINK` &rarr; `CREDENTIAL_REQUEST` &rarr; `OTP_REQUEST`
2. **UPI Fraud**: `PAYMENT_LURE` &rarr; `UPI_LINK` &rarr; `URGENCY` &rarr; `PIN_OR_OTP_REQUEST`
3. **Fake Support**: `BANK_SUPPORT_IMPERSONATION` &rarr; `ALERT_DISPUTE` &rarr; `REMOTE_ACCESS_REQUEST` &rarr; `CREDENTIAL_REQUEST`
4. **Job Scam**: `JOB_OFFER` &rarr; `INITIAL_REWARD` &rarr; `REGISTRATION_FEE` &rarr; `PAYMENT_REQUEST`
5. **Electricity Scam**: `DISCONNECTION_THREAT` &rarr; `URGENCY` &rarr; `FAKE_OFFICER_CALL` &rarr; `PAYMENT_REQUEST`
6. **Digital Arrest**: `LAW_ENFORCEMENT_IMPERSONATION` &rarr; `CONTRABAND_ACCUSATION` &rarr; `DIGITAL_ARREST_THREAT` &rarr; `VERIFICATION_ESCROW_TRANSFER`

### Pillar 3: Scam DNA & Campaign Clustering
- Each detected pattern is fingerprinted via dense semantic vectors and hashed signals (e.g. `#UPI-KYC-042`).
- Evolving linguistic variations (such as changing bank names or minor greetings) map into the identical underlying Scam DNA.
- **Unsupervised Discovery (DBSCAN)**: Continuously clusters live incident vectors. Sudden influxes (&gt;30% weekly velocity) trigger an `EMERGING PATTERN` advisory.

### Pillar 4: Calibrated Risk Formula
The composite risk index ($R \in [0, 100]$) is computed via:
$$R = \text{clamp}\Big(0.45 \cdot S_{\text{ML}} + 0.25 \cdot S_{\text{Rule}} + 0.15 \cdot S_{\text{URL}} + 0.15 \cdot S_{\text{Workflow}}, 0, 100\Big)$$

**Risk Tiers:**
- `0 - 29`: **LOW** (Passive monitoring, normal communications)
- `30 - 59`: **MEDIUM** (Advisory caution, suspicious characteristics present)
- `60 - 79`: **HIGH** (Strong alert, multi-signal fraud pattern)
- `80 - 100`: **CRITICAL** (Immediate intervention, multi-stage financial threat)

### Pillar 5: Privacy by Design
- In-memory regex sanitization automatically masks card numbers, CVVs, passwords, and OTP codes before logging or storage.
- Identifier hashing replaces phone numbers and emails with non-reversible cryptographic hashes.
- Interactive **Purge Incident Logs** endpoint allows instantaneous privacy erasure.
