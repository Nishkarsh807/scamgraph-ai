"""
ScamGraph AI - ML Inference Engine
Loads trained models, executes dual-head classification (Binary Fraud + Category),
and produces calibrated scam confidence.
"""

import os
import joblib
from typing import Dict, Any
try:
    from .preprocess import normalize_text, extract_entities, detect_language
except ImportError:
    from preprocess import normalize_text, extract_entities, detect_language

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "ml", "saved_models")

class ScamMLInference:
    _instance = None

    def __init__(self):
        self.binary_model_path = os.path.join(SAVED_MODELS_DIR, "binary_scam_model.joblib")
        self.category_model_path = os.path.join(SAVED_MODELS_DIR, "category_classifier.joblib")
        self.binary_model = None
        self.category_model = None
        self._load_models()

    def _load_models(self):
        if os.path.exists(self.binary_model_path):
            self.binary_model = joblib.load(self.binary_model_path)
        if os.path.exists(self.category_model_path):
            self.category_model = joblib.load(self.category_model_path)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Runs complete ML prediction pipeline on input text.
        """
        cleaned_text = normalize_text(text)
        language = detect_language(text)
        entities = extract_entities(text)

        if not self.binary_model or not self.category_model:
            self._load_models()

        if self.binary_model is None or self.category_model is None:
            return {
                "scam_probability": 0.5,
                "is_scam": False,
                "category": "OTHER",
                "category_confidence": 0.5,
                "language": language,
                "entities": entities
            }

        # Binary prediction (0 = Benign, 1 = Scam)
        probs = self.binary_model.predict_proba([cleaned_text])[0]
        scam_prob = float(probs[1])
        is_scam = bool(scam_prob >= 0.50)

        # Category prediction
        cat_probs = self.category_model.predict_proba([cleaned_text])[0]
        cat_classes = self.category_model.classes_
        top_idx = cat_probs.argmax()
        top_cat = str(cat_classes[top_idx]).upper()
        top_cat_conf = float(cat_probs[top_idx])

        # Top 3 category breakdown
        sorted_indices = cat_probs.argsort()[::-1][:3]
        top_categories = [
            {"category": str(cat_classes[idx]).upper(), "confidence": round(float(cat_probs[idx]), 3)}
            for idx in sorted_indices
        ]

        return {
            "scam_probability": round(scam_prob, 4),
            "is_scam": is_scam,
            "category": top_cat,
            "category_confidence": round(top_cat_conf, 4),
            "top_categories": top_categories,
            "language": language,
            "entities": entities
        }

# Global singleton
inference_engine = ScamMLInference.get_instance()
