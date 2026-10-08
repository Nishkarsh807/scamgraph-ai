"""
ScamGraph AI - Adaptive Alert Fatigue & Campaign Deduplication Engine
Regulates alert intensity according to risk thresholds and suppresses repetitive
alert fatigue by aggregating recurring incidents under active Scam DNA campaigns.
"""

from typing import Dict, Any
import time

class AlertEngine:
    def __init__(self):
        # Campaign detection counter: {dna_id: count}
        self.campaign_seen_counts: Dict[str, int] = {
            "UPI-KYC-042": 117,
            "ELEC-DISCONN-019": 83,
            "CYBER-ARREST-104": 64,
            "TASK-JOB-088": 142,
            "UPI-COLLECT-019": 92
        }

    def process_alert(self, risk_level: str, scam_dna: str, risk_score: int) -> Dict[str, Any]:
        """
        Calculates adaptive intervention modal style and deduplication notices.
        """
        clean_dna = scam_dna.replace("#", "").strip()

        # Update or record campaign frequency
        current_count = self.campaign_seen_counts.get(clean_dna, 0) + 1
        self.campaign_seen_counts[clean_dna] = current_count

        # Adaptive alert tiering
        if risk_level == "CRITICAL":
            alert_header = "STOP — Potential Financial Scam"
            intervention_type = "BLOCKING_INTERVENTION"
            user_guidance = "Immediate threat to funds or account security. Cease interaction immediately."
        elif risk_level == "HIGH":
            alert_header = "High Risk Scam Pattern Detected"
            intervention_type = "STRONG_WARNING"
            user_guidance = "Multiple deceptive indicators detected. Do not click links or disclose confidential data."
        elif risk_level == "MEDIUM":
            alert_header = "Caution: Suspicious Elements Present"
            intervention_type = "ADVISORY_WARNING"
            user_guidance = "Be careful before interacting. Verify authenticity through official channels."
        else:
            alert_header = "Normal / Low Risk Communication"
            intervention_type = "PASSIVE_MONITORING"
            user_guidance = "No severe scam indicators observed. Standard vigilance advised."

        # Deduplication intelligence
        is_repeat_campaign = current_count > 1
        if is_repeat_campaign:
            dedup_message = f"🛡️ {current_count} similar messages detected from active campaign ({scam_dna})."
        else:
            dedup_message = "First encounter with this unique pattern."

        return {
            "alert_header": alert_header,
            "intervention_type": intervention_type,
            "user_guidance": user_guidance,
            "is_repeat_campaign": is_repeat_campaign,
            "campaign_total_detected": current_count,
            "dedup_notice": dedup_message
        }


alert_engine = AlertEngine()
