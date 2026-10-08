"""
ScamGraph AI - Rule & Signal Extraction Engine
Provides deterministic evidence signals alongside ML model predictions.
"""

from typing import Dict, Any, List
import re

class SignalEngine:
    def __init__(self):
        self.signal_weights = {
            "urgency": 15,
            "threat": 20,
            "otp_request": 25,
            "kyc_request": 20,
            "payment_request": 20,
            "suspicious_url": 20,
            "impersonation": 15,
            "credential_request": 25,
            "reward_lure": 15,
            "phone_contact": 10,
            "unknown_sender": 10
        }

    def analyze(self, text: str, entities: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Calculates signal flags and weighted deterministic rule score (0-100).
        """
        lower = text.lower()
        if entities is None:
            entities = {}

        # 1. Signals detection
        signals = {
            "urgency": 0,
            "threat": 0,
            "otp_request": 0,
            "kyc_request": 0,
            "payment_request": 0,
            "suspicious_url": 0,
            "unknown_sender": 0,
            "impersonation": 0,
            "credential_request": 0,
            "reward_lure": 0,
            "phone_contact": 0
        }

        # Urgency
        urgency_terms = [
            "urgent", "immediately", "turant", "jaldi", "today", "tonight", "right now",
            "24 hours", "12 hours", "2 hours", "10 mins", "expires", "expiring", "expired",
            "deadline", "warning", "last chance", "final notice", "immediate", "aaj raat", "abhi"
        ]
        if any(w in lower for w in urgency_terms):
            signals["urgency"] = 1

        # Threat
        threat_terms = [
            "blocked", "block", "freeze", "deactivated", "deactivate", "disabled", "disconnected", "suspended",
            "digital arrest", "police", "cyber crime", "cbi", "arrest warrant", "summons",
            "customs", "penalty", "seized", "court", "interrogation", "kaat di jayegi", "band ho jayega"
        ]
        if any(w in lower for w in threat_terms):
            signals["threat"] = 1

        # KYC request
        kyc_terms = ["kyc", "aadhaar", "pan card", "pan & aadhaar", "biometric", "update kyc", "re-kyc", "yono"]
        if any(w in lower for w in kyc_terms):
            signals["kyc_request"] = 1

        # OTP request
        otp_terms = [
            "otp", "one time password", "secret pin", "6-digit", "verification code",
            "security token", "share otp", "tell the otp", "forward the code", "aaya hua otp"
        ]
        if any(w in lower for w in otp_terms):
            signals["otp_request"] = 1

        # Payment request
        payment_terms = [
            "pay", "transfer", "deposit", "send money", "processing fee", "registration fee",
            "gate pass fee", "stamp duty", "clearance fee", "qr code", "collect request",
            "approve mandate", "upi pin", "tax amount", "jama karein"
        ]
        if any(w in lower for w in payment_terms) or len(entities.get("upi_ids", [])) > 0:
            signals["payment_request"] = 1

        # Suspicious URL presence
        if len(entities.get("urls", [])) > 0:
            signals["suspicious_url"] = 1

        # Unknown / Suspicious sender indicators
        if signals["urgency"] or signals["threat"] or signals["suspicious_url"]:
            signals["unknown_sender"] = 1

        # Impersonation
        impersonation_terms = [
            "police", "cbi", "customs", "cyber crime", "sbi support", "hdfc bank",
            "bank manager", "army", "ceo", "hr department", "mahavitaran", "uppcl", "bses"
        ]
        if any(re.search(r'\b' + re.escape(w) + r'\b', lower) for w in impersonation_terms):
            signals["impersonation"] = 1

        # Credential / Sensitive request
        cred_terms = ["cvv", "expiry date", "card details", "password", "netbanking password", "anydesk", "quicksupport"]
        if any(w in lower for w in cred_terms):
            signals["credential_request"] = 1

        # Reward / Lure
        reward_terms = ["lottery", "cashback", "won", "scratch card", "lucky draw", "500% profit", "kbc", "inaam", "gift card"]
        if any(w in lower for w in reward_terms):
            signals["reward_lure"] = 1

        # Phone contact
        if len(entities.get("phone_numbers", [])) > 0:
            signals["phone_contact"] = 1

        # Calculate weighted rule score (capped at 100)
        total_score = sum(signals[sig] * self.signal_weights.get(sig, 10) for sig in signals)
        # Normalize: maximum potential raw sum is ~195, scale so ~3-4 strong signals yield 75-90
        normalized_score = min(100.0, round((total_score / 130.0) * 100, 1))

        # Human-readable detected signal list
        detected_list = [sig for sig, active in signals.items() if active == 1]

        return {
            "signals": signals,
            "detected_signals": detected_list,
            "rule_score": normalized_score,
            "total_signals_detected": len(detected_list)
        }

signal_engine = SignalEngine()
