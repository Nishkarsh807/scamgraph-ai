"""
ScamGraph AI - Scam Workflow Intelligence Engine
Tracks event sequences across multi-step scam playbooks, performs partial-order
and event alignment matching, predicts current stage and next attacker move.
"""

from typing import List, Dict, Any, Optional
import re

# Canonical Scam Workflow Definitions
WORKFLOW_PLAYBOOKS = {
    "KYC_FRAUD": {
        "title": "KYC Account Takeover Scam",
        "category": "KYC",
        "description": "Exploits anxiety regarding bank account suspension to extract credentials and OTP.",
        "canonical_steps": [
            "KYC_WARNING",
            "URGENCY",
            "EXTERNAL_LINK",
            "CREDENTIAL_REQUEST",
            "OTP_REQUEST",
            "UNAUTHORIZED_TRANSACTION"
        ],
        "default_dna": "UPI-KYC-042"
    },
    "UPI_FRAUD": {
        "title": "Reverse Payment / UPI Collect Fraud",
        "category": "UPI",
        "description": "Tricks victim into believing they are receiving money by making them enter their UPI PIN.",
        "canonical_steps": [
            "PAYMENT_LURE",
            "UPI_LINK",
            "URGENCY",
            "PIN_OR_OTP_REQUEST",
            "FINANCIAL_DRAIN"
        ],
        "default_dna": "UPI-COLLECT-019"
    },
    "FAKE_SUPPORT": {
        "title": "Remote Access Tech/Bank Support Scam",
        "category": "BANKING",
        "description": "Impersonates bank or customer service to install remote desktop tools and steal tokens.",
        "canonical_steps": [
            "BANK_SUPPORT_IMPERSONATION",
            "ALERT_DISPUTE_CLAIM",
            "REMOTE_ACCESS_REQUEST",
            "CREDENTIAL_REQUEST",
            "ACCOUNT_COMPROMISE"
        ],
        "default_dna": "SUPP-REMOTE-007"
    },
    "JOB_SCAM": {
        "title": "Part-Time Task & VIP Investment Trap",
        "category": "JOB",
        "description": "Initial small payouts for liking videos followed by escalating deposit demands to unlock funds.",
        "canonical_steps": [
            "JOB_OFFER",
            "INITIAL_REWARD",
            "REGISTRATION_OR_VIP_FEE",
            "PAYMENT_REQUEST",
            "EXTORTION_LOCKOUT"
        ],
        "default_dna": "TASK-JOB-088"
    },
    "ELECTRICITY_BILL": {
        "title": "Electricity Disconnection Panic Scam",
        "category": "ELECTRICITY",
        "description": "Threatens immediate power outage at night unless victim contacts fake officer or downloads app.",
        "canonical_steps": [
            "DISCONNECTION_THREAT",
            "URGENCY",
            "FAKE_OFFICER_CALL",
            "TOKEN_PAYMENT_REQUEST",
            "OTP_DRAIN"
        ],
        "default_dna": "ELEC-DISCONN-019"
    },
    "DIGITAL_ARREST": {
        "title": "Law Enforcement Digital Arrest Extortion",
        "category": "DIGITAL_ARREST",
        "description": "Fakes customs/police video interrogations accusing victim of contraband parcels to force fund transfer.",
        "canonical_steps": [
            "LAW_ENFORCEMENT_IMPERSONATION",
            "CONTRABAND_ACCUSATION",
            "DIGITAL_ARREST_THREAT",
            "VIDEO_INTERROGATION",
            "VERIFICATION_ESCROW_TRANSFER"
        ],
        "default_dna": "CYBER-ARREST-104"
    },
    "LOAN_SCAM": {
        "title": "Pre-Approved Loan Processing Advance-Fee Fraud",
        "category": "LOAN",
        "description": "Promises instant collateral-free loans but demands advance processing/GST fee via UPI.",
        "canonical_steps": [
            "LOAN_OFFER",
            "INSTANT_APPROVAL",
            "PROCESSING_FEE_REQUEST",
            "PAYMENT_REQUEST",
            "GHOSTING"
        ],
        "default_dna": "LOAN-ADVANCE-031"
    },
    "LOTTERY_CASHBACK": {
        "title": "KBC / Lucky Draw Prize Advance Tax Scam",
        "category": "LOTTERY",
        "description": "Notifies of huge prize wins requiring GST or release fees to be sent to private UPI handles.",
        "canonical_steps": [
            "LOTTERY_WIN_ANNOUNCEMENT",
            "WHATSAPP_CONTACT_DIRECTIVE",
            "TAX_OR_CLEARANCE_FEE",
            "PAYMENT_REQUEST",
            "SECONDARY_EXTORTION"
        ],
        "default_dna": "KBC-LUCKY-055"
    }
}


class ScamWorkflowEngine:
    def __init__(self):
        self.playbooks = WORKFLOW_PLAYBOOKS

    def extract_events_from_text(self, text: str, entities: Dict[str, Any], signals: Dict[str, int]) -> List[str]:
        """
        Derives fine-grained chronological or co-occurring workflow events.
        """
        lower = text.lower()
        events = []

        # KYC Warning
        if signals.get("kyc_request") or "kyc" in lower or "yono" in lower:
            events.append("KYC_WARNING")

        # Disconnection Threat
        if "bijli" in lower or "power" in lower or "electricity" in lower or "disconnected" in lower:
            if "bill" in lower or "meter" in lower or "sub-station" in lower:
                events.append("DISCONNECTION_THREAT")

        # Digital Arrest / Law Enforcement
        if any(w in lower for w in ["digital arrest", "police", "customs", "cbi", "cyber crime", "warrant", "mdma"]):
            events.append("LAW_ENFORCEMENT_IMPERSONATION")
            if any(w in lower for w in ["parcel", "drugs", "contraband", "passports", "laundering"]):
                events.append("CONTRABAND_ACCUSATION")
            if "digital arrest" in lower or "skype" in lower or "interrogation" in lower:
                events.append("DIGITAL_ARREST_THREAT")

        # Job Offer / Lottery Win
        if any(w in lower for w in ["part time", "work from home", "earn ₹", "youtube video", "hiring"]):
            events.append("JOB_OFFER")
        if any(w in lower for w in ["won", "lottery", "kbc", "lucky draw", "scratch card"]):
            events.append("LOTTERY_WIN_ANNOUNCEMENT")

        # Loan offer
        if "loan" in lower and any(w in lower for w in ["approved", "pre-approved", "sanction", "disburse"]):
            events.append("LOAN_OFFER")

        # Urgency
        if signals.get("urgency"):
            events.append("URGENCY")

        # External Link
        if signals.get("suspicious_url") or len(entities.get("urls", [])) > 0:
            events.append("EXTERNAL_LINK")

        # Support impersonation / Remote access
        if any(w in lower for w in ["anydesk", "quicksupport", "teamviewer"]):
            events.append("REMOTE_ACCESS_REQUEST")
        elif signals.get("impersonation") and any(w in lower for w in ["customer care", "helpline", "executive", "support"]):
            events.append("BANK_SUPPORT_IMPERSONATION")

        # Advance fee / Registration fee
        if any(w in lower for w in ["registration fee", "processing fee", "tax amount", "gate pass fee", "stamp duty"]):
            events.append("REGISTRATION_OR_ADVANCE_FEE")

        # Credential / Sensitive request
        if signals.get("credential_request") or any(w in lower for w in ["cvv", "card details", "password"]):
            events.append("CREDENTIAL_REQUEST")

        # OTP Request
        if signals.get("otp_request"):
            events.append("OTP_REQUEST")

        # UPI / Payment Request
        if len(entities.get("upi_ids", [])) > 0 or "upi pin" in lower or "collect request" in lower or "qr code" in lower:
            events.append("UPI_REQUEST")
        elif signals.get("payment_request"):
            events.append("PAYMENT_REQUEST")

        # Deduplicate while preserving sequence
        deduped = []
        for e in events:
            if e not in deduped:
                deduped.append(e)

        return deduped

    def evaluate_workflow(self, events: List[str], predicted_category: Optional[str] = None) -> Dict[str, Any]:
        """
        Matches detected events against workflow playbooks, evaluates completion percentage,
        identifies current stage and calculates workflow risk score.
        """
        if not events:
            return {
                "workflow_detected": False,
                "playbook_id": "NONE",
                "title": "No Cohesive Workflow",
                "confidence": 0.0,
                "workflow_score": 0.0,
                "detected_events": [],
                "canonical_workflow": [],
                "current_stage": "INITIAL_MONITORING",
                "next_predicted_threat": "None observed",
                "scam_dna": "DNA-CLEAN-000"
            }

        best_match = None
        best_score = -1.0
        events_set = set(events)

        # Evaluate similarity against playbooks
        for pb_key, pb_data in self.playbooks.items():
            canonical = pb_data["canonical_steps"]
            canonical_set = set(canonical)

            # Intersection
            overlap = events_set.intersection(canonical_set)
            if not overlap:
                continue

            # Jaccard + sequence alignment bonus
            jaccard = len(overlap) / len(canonical_set)
            
            # Boost if predicted ML category aligns with playbook
            cat_bonus = 0.20 if predicted_category and pb_data["category"].upper() in predicted_category.upper() else 0.0
            
            match_score = (jaccard * 0.8) + cat_bonus

            if match_score > best_score:
                best_score = match_score
                best_match = (pb_key, pb_data, overlap)

        if not best_match or len(best_match[2]) == 0:
            # Fallback workflow representation
            return {
                "workflow_detected": len(events) >= 2,
                "playbook_id": "GENERIC_SUSPICIOUS",
                "title": "Suspicious Multi-Signal Pattern",
                "confidence": min(0.70, len(events) * 0.25),
                "workflow_score": min(65.0, len(events) * 20.0),
                "detected_events": events,
                "canonical_workflow": events,
                "current_stage": f"Step {len(events)} of Multi-Vector Attempt",
                "next_predicted_threat": "Attempted sensitive information harvesting or payment redirect",
                "scam_dna": "GEN-SUSP-001"
            }

        pb_key, pb_data, overlap = best_match
        canonical = pb_data["canonical_steps"]

        # Calculate exact progression
        matched_indices = [canonical.index(e) for e in overlap if e in canonical]
        furthest_step_idx = max(matched_indices) if matched_indices else 0
        current_step_name = canonical[furthest_step_idx]

        # Predict next threat
        if furthest_step_idx + 1 < len(canonical):
            next_step = canonical[furthest_step_idx + 1]
            next_threat_desc = f"Attacker will attempt '{next_step.replace('_', ' ').title()}' to complete fraud."
        else:
            next_threat_desc = "Final fraud execution stage reached. Immediate fund/data loss risk."

        # Confidence computation
        confidence = min(0.99, round(0.50 + (len(overlap) / len(canonical)) * 0.45, 2))
        workflow_score = min(100.0, round(confidence * 100, 1))

        return {
            "workflow_detected": True,
            "playbook_id": pb_key,
            "title": pb_data["title"],
            "description": pb_data["description"],
            "confidence": confidence,
            "workflow_score": workflow_score,
            "detected_events": events,
            "canonical_workflow": canonical,
            "matched_steps_count": len(overlap),
            "total_canonical_steps": len(canonical),
            "current_stage": f"Stage {furthest_step_idx + 1}: {current_step_name.replace('_', ' ').title()}",
            "next_predicted_threat": next_threat_desc,
            "scam_dna": pb_data["default_dna"]
        }


workflow_engine = ScamWorkflowEngine()
