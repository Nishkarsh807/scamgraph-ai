"""
ScamGraph AI - Risk Score & Explanation Engine
Combines ML probability, rule-based heuristics, URL threat analysis,
and multi-step workflow alignment into a calibrated 0-100 risk score,
risk tiers, and human-comprehensible evidence explanations.
"""

from typing import Dict, Any, List

class RiskEngine:
    def __init__(self):
        # Configurable production weights
        self.w_ml = 0.45
        self.w_rule = 0.25
        self.w_url = 0.15
        self.w_workflow = 0.15

    def calculate_risk(
        self,
        ml_prob: float,
        rule_score: float,
        url_score: float,
        workflow_score: float,
        signals_detected: List[str]
    ) -> Dict[str, Any]:
        """
        Computes composite risk score (0-100), risk tier, and explainable breakdowns.
        """
        # ML score is 0.0 - 1.0 -> scale to 0-100
        ml_scaled = ml_prob * 100.0

        raw_final = (
            (self.w_ml * ml_scaled) +
            (self.w_rule * rule_score) +
            (self.w_url * url_score) +
            (self.w_workflow * workflow_score)
        )

        # Cap between 0 and 100
        final_score = int(round(max(0.0, min(100.0, raw_final))))

        # Classify risk level
        if final_score >= 80:
            risk_level = "CRITICAL"
            badge_color = "red"
        elif final_score >= 60:
            risk_level = "HIGH"
            badge_color = "orange"
        elif final_score >= 30:
            risk_level = "MEDIUM"
            badge_color = "yellow"
        else:
            risk_level = "LOW"
            badge_color = "green"

        return {
            "risk_score": final_score,
            "risk_level": risk_level,
            "badge_color": badge_color,
            "breakdown": {
                "ml_component": round(self.w_ml * ml_scaled, 1),
                "rule_component": round(self.w_rule * rule_score, 1),
                "url_component": round(self.w_url * url_score, 1),
                "workflow_component": round(self.w_workflow * workflow_score, 1)
            }
        }

    def generate_explanation(
        self,
        scam_type: str,
        risk_level: str,
        signals: List[str],
        events: List[str],
        url_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Builds explainable narrative and specific actionable safety recommendation.
        """
        signal_readable = {
            "urgency": "Urgency pressure (forcing hurried decisions)",
            "threat": "Account freeze or legal consequence threat",
            "kyc_request": "Unsolicited KYC / Aadhaar / PAN update demand",
            "otp_request": "One-Time Password (OTP) or PIN request",
            "payment_request": "Advance fee or unexpected fund transfer request",
            "suspicious_url": "Untrusted external link or malicious domain",
            "impersonation": "Impersonation of financial institution or government body",
            "credential_request": "Demand for card CVV, passwords, or remote access",
            "reward_lure": "Unrealistic lottery, reward, or high-return promise",
            "phone_contact": "Direct contact request to unverified mobile number"
        }

        reasons = [signal_readable[s] for s in signals if s in signal_readable]
        if not reasons:
            reasons = ["Normal conversational or verified informational characteristics."]

        # Actionable recommendations based on detected category
        recommendations = {
            "KYC": "Do NOT click the verification link or share your OTP. Open your bank's official app directly or visit your local branch to check your KYC status.",
            "UPI": "NEVER enter your UPI PIN or accept collect requests to receive money. Receiving funds never requires entering a secret PIN.",
            "OTP": "STOP immediately. Never read out or forward an OTP. Bank employees and delivery personnel will NEVER ask for your login or card OTP.",
            "PHISHING": "Do not enter login credentials or download attachments. Check the sender domain carefully and navigate directly to the official portal.",
            "BANKING": "Do not install AnyDesk, TeamViewer, or QuickSupport tools. Contact your bank exclusively via the toll-free number printed on your debit card.",
            "JOB": "Do not pay any upfront 'registration fee' or 'VIP task deposit'. Legitimate companies will never charge candidates to work.",
            "ELECTRICITY": "Power companies do not send WhatsApp/SMS threats to disconnect power at night with personal mobile numbers. Verify dues on your official electricity board portal.",
            "DIGITAL_ARREST": "Law enforcement agencies (Police, CBI, Customs) do NOT conduct arrests or interrogations over Skype/WhatsApp video calls, nor do they ask you to deposit money in 'escrow' accounts.",
            "LOAN": "Never pay advance 'processing fees' or 'stamp duty' via UPI before receiving a loan. Registered lenders deduct fees from the disbursed loan amount.",
            "LOTTERY": "Ignore prize claims requiring advance GST or customs payment. Legitimate lotteries deduct government taxes at source.",
            "IMPERSONATION": "Call the person or institution directly on their verified official phone number to confirm identity before transferring money.",
            "OTHER": "Exercise caution. Verify the sender's identity through official independent channels before taking action."
        }

        cat_key = scam_type.upper().replace("_FRAUD", "")
        rec_text = recommendations.get(cat_key, recommendations["OTHER"])

        return {
            "summary": f"This interaction appears {risk_level.lower()} because it combines " +
                       f"{', '.join(reasons[:3]).lower()}.",
            "evidence_reasons": reasons,
            "recommended_action": rec_text
        }


risk_engine = RiskEngine()
