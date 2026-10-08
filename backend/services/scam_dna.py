"""
ScamGraph AI - Scam DNA & Semantic Fingerprint Engine
Generates semantic embeddings, fingerprints scam campaigns using vector similarity,
and links variations of identical scams to shared Scam DNA identifiers.
"""

import os
import hashlib
import numpy as np
from typing import Dict, Any, List, Tuple

# Baseline Scam DNA Fingerprint Registry with prototype descriptions
DNA_REGISTRY = [
    {
        "dna_id": "UPI-KYC-042",
        "campaign_name": "YONO & Bank KYC Expiry APK/Phishing Network",
        "category": "KYC",
        "signals": ["kyc_request", "urgency", "threat", "suspicious_url", "otp_request"],
        "prototype_phrases": [
            "Your SBI KYC will expire today. Update immediately.",
            "Dear customer, your bank account is suspended due to pending KYC.",
            "Aapka SBI account block ho jayega, KYC update karein turant link par."
        ],
        "active_cases": 117,
        "weekly_growth": "+64%",
        "risk_level": "CRITICAL"
    },
    {
        "dna_id": "ELEC-DISCONN-019",
        "campaign_name": "Evening Electricity Disconnection Threat",
        "category": "ELECTRICITY",
        "signals": ["threat", "urgency", "phone_contact", "payment_request"],
        "prototype_phrases": [
            "Electricity will be disconnected tonight at 9:30 PM due to unpaid bill.",
            "Priye upbhokta, aapki bijli aaj raat kaat di jayegi. Call officer Sharma.",
            "Power supply disconnected from sub-station. Pay verification bill."
        ],
        "active_cases": 83,
        "weekly_growth": "+41%",
        "risk_level": "HIGH"
    },
    {
        "dna_id": "CYBER-ARREST-104",
        "campaign_name": "CBI & Customs Airport Contraband Digital Arrest",
        "category": "DIGITAL_ARREST",
        "signals": ["threat", "impersonation", "payment_request"],
        "prototype_phrases": [
            "Inspector Rajesh Kumar Cyber Crime Branch FedEx parcel seized MDMA drugs.",
            "You are under digital arrest by CBI. Connect on Skype video interrogation.",
            "Arrest warrant issued against Aadhaar card for laundering transfer funds."
        ],
        "active_cases": 64,
        "weekly_growth": "+78%",
        "risk_level": "CRITICAL"
    },
    {
        "dna_id": "UPI-COLLECT-019",
        "campaign_name": "Reverse Collect Request / Army OLX Furniture Buyer",
        "category": "UPI",
        "signals": ["payment_request", "urgency", "reward_lure"],
        "prototype_phrases": [
            "I have sent UPI QR code scan and enter UPI PIN to receive ₹15,000.",
            "Accept collect request and enter secret PIN to claim cashback into bank.",
            "Paise receive karne ke liye Google Pay par QR scan karein PIN enter karein."
        ],
        "active_cases": 92,
        "weekly_growth": "+32%",
        "risk_level": "HIGH"
    },
    {
        "dna_id": "TASK-JOB-088",
        "campaign_name": "Telegram YouTube Like Video / VIP Task Trap",
        "category": "JOB",
        "signals": ["reward_lure", "payment_request"],
        "prototype_phrases": [
            "Earn ₹2,000 to ₹5,000 daily working from home liking YouTube videos Telegram.",
            "Work from home task job like 3 reels get ₹150 deposit VIP trading task.",
            "Part time job opportunity evaluate Amazon products WhatsApp."
        ],
        "active_cases": 142,
        "weekly_growth": "+55%",
        "risk_level": "HIGH"
    },
    {
        "dna_id": "LOAN-ADVANCE-031",
        "campaign_name": "Instant Pre-Approved Aadhaar Loan Processing Fee",
        "category": "LOAN",
        "signals": ["payment_request", "urgency", "reward_lure"],
        "prototype_phrases": [
            "Instant personal loan ₹5,00,000 approved at 2% pay processing fee ₹1,999.",
            "Aapka pre-approved loan pass ho gaya hai processing fee jama karein.",
            "Dhani loan sanction letter ready pay insurance charge to disburse."
        ],
        "active_cases": 58,
        "weekly_growth": "+18%",
        "risk_level": "MEDIUM"
    },
    {
        "dna_id": "KBC-LUCKY-055",
        "campaign_name": "KBC WhatsApp Lucky Draw Advance GST Scam",
        "category": "LOTTERY",
        "signals": ["reward_lure", "payment_request", "phone_contact"],
        "prototype_phrases": [
            "KBC WhatsApp number won ₹25,00,000 lucky draw contact Rana Pratap.",
            "Badhai ho mobile number ko Jio lucky draw mein inaam mila hai GST fee bhejo.",
            "Congratulations grand winner of ₹10,00,000 transfer government GST amount."
        ],
        "active_cases": 76,
        "weekly_growth": "+22%",
        "risk_level": "HIGH"
    }
]


class ScamDNAEngine:
    _instance = None

    def __init__(self):
        self.registry = DNA_REGISTRY
        self.embedder = None
        self._init_embedder()
        self.registry_embeddings = self._precompute_registry_embeddings()

    def _init_embedder(self):
        try:
            from sentence_transformers import SentenceTransformer
            # Use small, lightning-fast embedding model
            self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
            print("Loaded SentenceTransformer for Scam DNA matching.")
        except Exception as e:
            print(f"Notice: SentenceTransformer offline fallback will use lexical/ngram embedding: {e}")
            self.embedder = None

    def get_embedding(self, text: str) -> np.ndarray:
        if self.embedder is not None:
            try:
                emb = self.embedder.encode(text, convert_to_numpy=True)
                # Normalize
                norm = np.linalg.norm(emb)
                return emb / (norm + 1e-9)
            except Exception:
                pass
        
        # Robust lightweight TF-IDF / Subword hashing fallback
        vec = np.zeros(128, dtype=np.float32)
        words = text.lower().split()
        for w in words:
            h = int(hashlib.md5(w.encode('utf-8')).hexdigest(), 16) % 128
            vec[h] += 1.0
        norm = np.linalg.norm(vec)
        return vec / (norm + 1e-9)

    def _precompute_registry_embeddings(self) -> List[Tuple[Dict[str, Any], np.ndarray]]:
        results = []
        for reg in self.registry:
            joined_text = " ".join(reg["prototype_phrases"]) + " " + " ".join(reg["signals"])
            emb = self.get_embedding(joined_text)
            results.append((reg, emb))
        return results

    def match_scam_dna(self, text: str, category: str, detected_signals: List[str]) -> Dict[str, Any]:
        """
        Calculates cosine similarity to match message to existing Scam DNA campaign
        or mints a new unique fingerprint.
        """
        query_emb = self.get_embedding(text)
        best_match = None
        best_sim = -1.0

        for reg, reg_emb in self.registry_embeddings:
            sim = float(np.dot(query_emb, reg_emb))
            
            # Boost if category matches
            if reg["category"].lower() in category.lower():
                sim += 0.15

            # Boost if shared signals
            shared_signals = set(detected_signals).intersection(set(reg["signals"]))
            sim += (len(shared_signals) * 0.05)

            if sim > best_sim:
                best_sim = sim
                best_match = reg

        # If similarity exceeds threshold
        if best_match and best_sim >= 0.50:
            dna_id = best_match["dna_id"]
            return {
                "scam_dna": f"#{dna_id}",
                "dna_id": dna_id,
                "campaign_name": best_match["campaign_name"],
                "similarity": round(min(0.99, best_sim), 3),
                "is_known_campaign": True,
                "active_reports": best_match["active_cases"],
                "weekly_growth": best_match["weekly_growth"],
                "risk_level": best_match["risk_level"]
            }

        # Otherwise synthesize fingerprint based on category and hash
        cat_prefix = category[:4].upper() if category else "GEN"
        hash_suffix = hashlib.md5(text.encode()).hexdigest()[:3].upper()
        new_dna = f"#{cat_prefix}-VAR-{hash_suffix}"

        return {
            "scam_dna": new_dna,
            "dna_id": new_dna.replace("#", ""),
            "campaign_name": f"Emerging {category.title()} Variant",
            "similarity": 0.42,
            "is_known_campaign": False,
            "active_reports": 1,
            "weekly_growth": "+0%",
            "risk_level": "HIGH"
        }

    def get_all_patterns(self) -> List[Dict[str, Any]]:
        return self.registry


scam_dna_engine = ScamDNAEngine()
