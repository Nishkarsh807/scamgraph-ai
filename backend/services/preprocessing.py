"""
ScamGraph AI - Preprocessing Service
"""

import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(BASE_DIR, "ml"))
from preprocess import normalize_text, extract_entities, detect_language, extract_signal_flags

class PreprocessService:
    def process(self, text: str):
        cleaned = normalize_text(text)
        entities = extract_entities(text)
        lang = detect_language(text)
        return {
            "cleaned_text": cleaned,
            "entities": entities,
            "language": lang
        }

preprocess_service = PreprocessService()
