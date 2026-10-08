"""
ScamGraph AI - Comprehensive Unit & Integration Test Suite
Validates:
1. Signal & Rule Engine
2. URL Analyzer
3. Workflow Engine & Playbook Matching
4. Privacy Redactor
5. End-to-End FastAPI Analyze Endpoint (KYC scam, UPI scam, Benign message)
6. Patterns & Dashboard Endpoints
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add backend and ml to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "backend"))
sys.path.append(os.path.join(BASE_DIR, "ml"))

from main import app
from services.signal_engine import signal_engine
from services.url_analyzer import url_analyzer
from services.workflow_engine import workflow_engine
from utils.redactor import redact_sensitive_info

client = TestClient(app)


def test_signal_engine_detection():
    text = "URGENT: Your SBI KYC has expired. Enter OTP immediately to avoid account block."
    res = signal_engine.analyze(text)
    assert res["signals"]["urgency"] == 1
    assert res["signals"]["kyc_request"] == 1
    assert res["signals"]["otp_request"] == 1
    assert res["signals"]["threat"] == 1
    assert res["rule_score"] >= 60.0


def test_url_analyzer():
    url = "http://sbi-kyc-verify.xyz/login"
    res = url_analyzer.analyze_url(url)
    assert res["is_suspicious"] is True
    assert res["is_suspicious_tld"] is True
    assert not res["is_https"]
    assert any("Impersonation" in f for f in res["flags"])
    assert res["risk_score"] >= 60.0


def test_privacy_redactor():
    sample = "My phone is 9876543210 and OTP is 492019. Card: 4111 2222 3333 4444 CVV: 891"
    redacted = redact_sensitive_info(sample)
    assert "492019" not in redacted
    assert "4111 2222 3333 4444" not in redacted
    assert "891" not in redacted
    assert "[REDACTED_CODE]" in redacted
    assert "[CARD_NUMBER_REDACTED]" in redacted


def test_workflow_engine_matching():
    events = ["KYC_WARNING", "URGENCY", "EXTERNAL_LINK", "OTP_REQUEST"]
    res = workflow_engine.evaluate_workflow(events, predicted_category="KYC")
    assert res["workflow_detected"] is True
    assert res["playbook_id"] == "KYC_FRAUD"
    assert res["confidence"] >= 0.75
    assert "UPI-KYC" in res["scam_dna"]


def test_api_analyze_kyc_scam():
    payload = {
        "text": "Your SBI KYC expired today. Click http://sbi-fake-login.xyz to verify or your account will be blocked.",
        "url": "http://sbi-fake-login.xyz"
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] >= 70
    assert data["risk_level"] in ["HIGH", "CRITICAL"]
    assert "KYC" in data["scam_type"]
    assert len(data["signals"]) >= 3
    assert "scam_graph" in data
    assert len(data["scam_graph"]["nodes"]) >= 3


def test_api_analyze_benign_message():
    payload = {
        "text": "Your SBI account XX3829 debited by INR 350.00 on 08-Oct-26 at SWIGGY. Avail Bal: INR 18,450.20."
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] < 40
    assert data["risk_level"] in ["LOW", "MEDIUM"]


def test_api_dashboard_and_patterns():
    dash_res = client.get("/api/dashboard")
    assert dash_res.status_code == 200
    dash_data = dash_res.json()
    assert dash_data["total_analyzed"] > 0
    assert "model_metrics" in dash_data

    pat_res = client.get("/api/patterns")
    assert pat_res.status_code == 200
    patterns = pat_res.json()
    assert len(patterns) >= 3
