# ScamGraph AI — API Reference

Base URL: `http://localhost:8000/api`

Interactive Swagger Docs: `http://localhost:8000/docs`

---

## Endpoints

### 1. Analyze Interaction
- **Path**: `POST /api/analyze`
- **Request Body**:
  ```json
  {
    "text": "Your SBI KYC expired today. Click http://sbi-fake.xyz to update or account will be blocked.",
    "url": "http://sbi-fake.xyz",
    "sender": "+919876543210"
  }
  ```
- **Response**:
  ```json
  {
    "risk_score": 91,
    "risk_level": "CRITICAL",
    "scam_type": "KYC_FRAUD",
    "confidence": 0.94,
    "signals": ["urgency", "threat", "kyc_request", "suspicious_url"],
    "workflow": ["KYC_WARNING", "URGENCY", "EXTERNAL_LINK"],
    "workflow_details": {
      "title": "KYC Account Takeover Scam",
      "current_stage": "Stage 3: External Link",
      "next_predicted_threat": "Attacker will attempt 'Credential Request' to complete fraud."
    },
    "scam_dna": "#UPI-KYC-042",
    "campaign_name": "YONO & Bank KYC Expiry APK/Phishing Network",
    "recommendation": "Do NOT click the verification link or share your OTP. Open your bank's official app directly.",
    "evidence_reasons": [
      "Urgency pressure (forcing hurried decisions)",
      "Account freeze or legal consequence threat",
      "Unsolicited KYC / Aadhaar / PAN update demand",
      "Untrusted external link or malicious domain"
    ],
    "entities": {
      "urls": ["http://sbi-fake.xyz"],
      "phone_numbers": ["+919876543210"],
      "upi_ids": [],
      "amounts": []
    },
    "url_analysis": {
      "hostname": "sbi-fake.xyz",
      "risk_score": 75.0,
      "flags": ["Insecure HTTP protocol", "Uncommon / high-abuse TLD (.xyz)", "Potential Brand Impersonation: SBI"]
    },
    "alert_details": {
      "alert_header": "STOP — Potential Financial Scam",
      "intervention_type": "BLOCKING_INTERVENTION",
      "is_repeat_campaign": true,
      "dedup_notice": "🛡️ 118 similar messages detected from active campaign (#UPI-KYC-042)."
    },
    "scam_graph": {
      "nodes": [...],
      "edges": [...]
    }
  }
  ```

---

### 2. Emerging Patterns
- **Path**: `GET /api/patterns`
- **Description**: Returns active clusters discovered by DBSCAN with growth velocity and timeline data.
- **Path**: `GET /api/patterns/{id}`
- **Description**: Detailed deep-dive into specific campaign fingerprint.

---

### 3. Dashboard Metrics
- **Path**: `GET /api/dashboard`
- **Description**: Returns overall telemetry, model evaluation benchmarks from `ml/reports/metrics.json`, and 7-day trend series.

---

### 4. Community Incident Reporting
- **Path**: `POST /api/report`
- **Description**: Submits an anonymized community scam tip.

---

### 5. Privacy History Erasure
- **Path**: `DELETE /api/incidents/clear`
- **Description**: Purges all stored incident records and analysis history.
