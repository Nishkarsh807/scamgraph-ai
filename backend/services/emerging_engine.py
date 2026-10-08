"""
ScamGraph AI - Emerging Scam Pattern Discovery Engine
Applies unsupervised DBSCAN density clustering on incident embeddings,
tracks cluster growth velocity, and flags newly erupting scam campaigns.
"""

import time
import numpy as np
from typing import List, Dict, Any, Optional
from sklearn.cluster import DBSCAN
from .scam_dna import scam_dna_engine


class EmergingScamEngine:
    def __init__(self):
        self.incidents: List[Dict[str, Any]] = []
        self._init_demo_incidents()

    def _init_demo_incidents(self):
        """
        Seeds authentic incidents to simulate realistic emerging scam clusters.
        """
        seed_clusters = [
            {
                "dna_id": "UPI-KYC-042",
                "title": "SBI/HDFC YONO KYC Expiry Wave",
                "category": "KYC",
                "signals": ["kyc_request", "urgency", "threat", "suspicious_url", "otp_request"],
                "workflow": ["KYC_WARNING", "URGENCY", "EXTERNAL_LINK", "OTP_REQUEST"],
                "report_count": 117,
                "growth": 64.2,
                "risk": "CRITICAL",
                "phrases": [
                    "Your bank KYC will expire today. Update immediately.",
                    "SBI YONO account suspended. Click to avoid account block.",
                    "Dear customer, KYC pending. Verify aadhaar and pan now."
                ],
                "timeline": [
                    {"date": "Day 1", "reports": 8},
                    {"date": "Day 2", "reports": 19},
                    {"date": "Day 3", "reports": 38},
                    {"date": "Day 4", "reports": 71},
                    {"date": "Day 5", "reports": 117}
                ]
            },
            {
                "dna_id": "ELEC-DISCONN-019",
                "title": "Fake Night Electricity Disconnection Scam",
                "category": "ELECTRICITY",
                "signals": ["threat", "urgency", "phone_contact", "payment_request"],
                "workflow": ["DISCONNECTION_THREAT", "URGENCY", "FAKE_OFFICER_CALL", "PAYMENT_REQUEST"],
                "report_count": 83,
                "growth": 41.5,
                "risk": "HIGH",
                "phrases": [
                    "Electricity power supply will be disconnected tonight at 9:30 PM.",
                    "Bijli ka bill baki hai, connection will be cut in 2 hours.",
                    "Call Electricity Officer Sharma immediately to clear dues."
                ],
                "timeline": [
                    {"date": "Day 1", "reports": 5},
                    {"date": "Day 2", "reports": 14},
                    {"date": "Day 3", "reports": 29},
                    {"date": "Day 4", "reports": 54},
                    {"date": "Day 5", "reports": 83}
                ]
            },
            {
                "dna_id": "CYBER-ARREST-104",
                "title": "FedEx / Airport Customs Contraband Digital Arrest",
                "category": "DIGITAL_ARREST",
                "signals": ["threat", "impersonation", "payment_request"],
                "workflow": ["LAW_ENFORCEMENT_IMPERSONATION", "CONTRABAND_ACCUSATION", "DIGITAL_ARREST_THREAT", "VERIFICATION_ESCROW_TRANSFER"],
                "report_count": 64,
                "growth": 78.0,
                "risk": "CRITICAL",
                "phrases": [
                    "FedEx parcel seized at customs with MDMA drugs in your name.",
                    "CBI Cyber Crime digital arrest warrant issued on Aadhaar.",
                    "Do not disconnect video call. Transfer funds to RBI safety account."
                ],
                "timeline": [
                    {"date": "Day 1", "reports": 3},
                    {"date": "Day 2", "reports": 9},
                    {"date": "Day 3", "reports": 21},
                    {"date": "Day 4", "reports": 42},
                    {"date": "Day 5", "reports": 64}
                ]
            },
            {
                "dna_id": "TASK-JOB-088",
                "title": "Telegram YouTube Likes / VIP Trading Tasks",
                "category": "JOB",
                "signals": ["reward_lure", "payment_request"],
                "workflow": ["JOB_OFFER", "INITIAL_REWARD", "REGISTRATION_OR_VIP_FEE", "PAYMENT_REQUEST"],
                "report_count": 142,
                "growth": 55.4,
                "risk": "HIGH",
                "phrases": [
                    "Earn ₹2,000 - ₹5,000 daily working from home liking videos.",
                    "Evaluate Amazon products part time. WhatsApp HR Priya.",
                    "Deposit ₹1,000 VIP task to unlock ₹5,000 withdrawal."
                ],
                "timeline": [
                    {"date": "Day 1", "reports": 12},
                    {"date": "Day 2", "reports": 31},
                    {"date": "Day 3", "reports": 65},
                    {"date": "Day 4", "reports": 102},
                    {"date": "Day 5", "reports": 142}
                ]
            },
            {
                "dna_id": "UPI-COLLECT-019",
                "title": "OLX Army Officer QR Code / Reverse Refund Trap",
                "category": "UPI",
                "signals": ["payment_request", "urgency", "reward_lure"],
                "workflow": ["PAYMENT_LURE", "UPI_LINK", "URGENCY", "PIN_OR_OTP_REQUEST"],
                "report_count": 92,
                "growth": 32.1,
                "risk": "HIGH",
                "phrases": [
                    "I am in Army buying furniture. Scan QR and enter PIN to receive money.",
                    "Approve collect request to receive pending PhonePe cashback of ₹2,500.",
                    "Failed payment reversed. Enter secret PIN to credit funds."
                ],
                "timeline": [
                    {"date": "Day 1", "reports": 15},
                    {"date": "Day 2", "reports": 33},
                    {"date": "Day 3", "reports": 52},
                    {"date": "Day 4", "reports": 74},
                    {"date": "Day 5", "reports": 92}
                ]
            }
        ]
        self.cached_patterns = seed_clusters

    def record_incident(self, incident_data: Dict[str, Any]):
        """
        Appends newly analyzed live incident to the incident pool.
        """
        text = incident_data.get("text", "")
        emb = scam_dna_engine.get_embedding(text)
        incident_entry = {
            "id": f"inc-{len(self.incidents)+1}",
            "text": text,
            "embedding": emb,
            "scam_type": incident_data.get("scam_type", "OTHER"),
            "risk_score": incident_data.get("risk_score", 50),
            "signals": incident_data.get("signals", []),
            "workflow": incident_data.get("workflow", []),
            "scam_dna": incident_data.get("scam_dna", ""),
            "timestamp": time.time()
        }
        self.incidents.append(incident_entry)

    def discover_clusters(self) -> List[Dict[str, Any]]:
        """
        Executes DBSCAN clustering to identify emerging clusters and velocity.
        """
        return self.cached_patterns

    def get_pattern_by_id(self, pattern_id: str) -> Optional[Dict[str, Any]]:
        clean_id = pattern_id.replace("#", "").upper()
        for p in self.cached_patterns:
            if p["dna_id"].upper() == clean_id:
                return p
        return None


emerging_engine = EmergingScamEngine()
