"""
ScamGraph AI - Data Preprocessing & Signal Extraction Core
Preserves critical scam signals (URLs, numbers, amounts, UPI IDs) while normalizing text.
Extracts structured indicators for both rule-based heuristics and ML inputs.
"""

import re
from typing import Dict, Any, List

# Regular expressions for entities
URL_PATTERN = re.compile(
    r'(?:https?://|www\.)[a-zA-Z0-9.\-]+(?:\.[a-zA-Z]{2,})+(?:[^\s,;"\'<>)]*)?',
    re.IGNORECASE
)
DOMAIN_ONLY_PATTERN = re.compile(
    r'\b(?:[a-zA-Z0-9\-]+\.)+(?:com|xyz|top|site|in|org|net|live|vip|biz|cc|apk|me|info|link|app|online)\b',
    re.IGNORECASE
)
PHONE_PATTERN = re.compile(
    r'(?:\+?91[\s\-]?)?(?:[6-9]\d{9})\b',
    re.IGNORECASE
)
UPI_PATTERN = re.compile(
    r'[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}',
    re.IGNORECASE
)
EMAIL_PATTERN = re.compile(
    r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    re.IGNORECASE
)
CURRENCY_PATTERN = re.compile(
    r'(?:₹|INR|Rs\.?|Rupees)\s*[\d,]+(?:\.\d{1,2})?(?:\s*(?:Crores?|Lakhs?|LPA|K))?',
    re.IGNORECASE
)

# Semantic dictionaries
URGENCY_KEYWORDS = [
    "urgent", "immediately", "turant", "jaldi", "today", "tonight", "right now",
    "24 hours", "12 hours", "2 hours", "10 mins", "expires", "expiring", "expired",
    "suspended", "deadline", "warning", "last chance", "final notice", "immediate",
    "aaj raat", "abhi", "freeze within", "act now"
]

THREAT_KEYWORDS = [
    "blocked", "freeze", "deactivated", "disabled", "disconnected", "suspended",
    "digital arrest", "police", "cyber crime", "cbi", "arrest warrant", "summons",
    "customs", "penalty", "seized", "mdma", "drugs", "illegal", "court", "interrogation",
    "kaat di jayegi", "band ho jayega", "penalty of", "punishment"
]

KYC_KEYWORDS = [
    "kyc", "aadhaar", "pan card", "pan & aadhaar", "biometric", "voter id",
    "document verification", "update kyc", "re-kyc", "kyc status", "yono", "wallet kyc",
    "biometric check", "kyc pending"
]

OTP_KEYWORDS = [
    "otp", "one time password", "secret pin", "6-digit", "verification code",
    "security token", "token code", "share otp", "tell the otp", "forward the code",
    "aaya hua otp", "pin code"
]

PAYMENT_REQUEST_KEYWORDS = [
    "pay", "transfer", "deposit", "send money", "processing fee", "registration fee",
    "gate pass fee", "stamp duty", "clearance fee", "insurance charge", "qr code",
    "collect request", "approve mandate", "upi pin", "enter upi pin", "scan qr",
    "tax amount", "jama karein", "approve karke"
]

SENSITIVE_INFO_KEYWORDS = [
    "cvv", "expiry date", "card number", "pin", "password", "netbanking password",
    "contact list", "card details", "biometric", "login credentials"
]

REWARD_LURE_KEYWORDS = [
    "lottery", "cashback", "reward", "won", "winner", "scratch card", "lucky draw",
    "500% profit", "guaranteed profit", "free gift", "daily return", "inaam",
    "badhai ho", "kbc", "iphone 15"
]

HINGLISH_KEYWORDS = [
    "aapka", "aapke", "turant", "karein", "kare", "khata", "bhejein", "paise", "galti",
    "varna", "hoga", "hai", "bhai", "bijli", "kaat", "inaam", "raat", "abhi", "par",
    "pe", "se", "humare", "sirf", "mahina", "dopahar", "shaam"
]


def detect_language(text: str) -> str:
    """Detect whether text is primarily English or Hinglish/Hindi Romanized."""
    lower = text.lower()
    hinglish_count = sum(1 for word in HINGLISH_KEYWORDS if re.search(r'\b' + re.escape(word) + r'\b', lower))
    return "hinglish" if hinglish_count >= 2 else "english"


def extract_entities(text: str) -> Dict[str, Any]:
    """
    Extract critical scam signals without dropping indicators.
    """
    urls = URL_PATTERN.findall(text)
    # Also look for standalone suspicious domains if no http/https
    domain_matches = DOMAIN_ONLY_PATTERN.findall(text)
    all_urls = list(dict.fromkeys(urls + [d for d in domain_matches if d not in " ".join(urls)]))

    # Phones
    phones = PHONE_PATTERN.findall(text)

    # UPI IDs (exclude standard emails if domain has .com/.org without upi handles)
    upi_candidates = UPI_PATTERN.findall(text)
    emails = EMAIL_PATTERN.findall(text)

    # Differentiate UPI IDs vs email addresses
    upi_handles = {'upi', 'oksbi', 'okhdfcbank', 'okicici', 'okaxis', 'paytm', 'ybl', 'apl', 'ibl', 'axl', 'barodampay'}
    upis = []
    clean_emails = []
    for cand in upi_candidates:
        handle = cand.split('@')[-1].lower()
        if handle in upi_handles or not re.search(r'\.(com|org|net|edu|gov)$', handle):
            upis.append(cand)
        else:
            clean_emails.append(cand)

    # Currencies / Amounts
    amounts = CURRENCY_PATTERN.findall(text)

    return {
        "urls": all_urls,
        "phone_numbers": phones,
        "upi_ids": upis,
        "emails": clean_emails,
        "amounts": amounts
    }


def normalize_text(text: str, preserve_signals: bool = True) -> str:
    """
    Clean whitespace and normalize quotes while strictly PRESERVING
    amounts, URLs, phone numbers, and case-sensitive indicators if needed.
    """
    if not text:
        return ""
    # Normalize unicode spaces and quotes
    cleaned = text.replace('\xa0', ' ').replace('“', '"').replace('”', '"').replace('’', "'")
    # Collapse excessive whitespace
    cleaned = re.sub(r'[ \t]+', ' ', cleaned)
    cleaned = re.sub(r'[\r\n]+', '\n', cleaned).strip()
    return cleaned


def extract_signal_flags(text: str, entities: Dict[str, Any] = None) -> Dict[str, int]:
    """
    Deterministic signal detection engine.
    Returns 0 or 1 for each signal indicator.
    """
    if entities is None:
        entities = extract_entities(text)
    
    lower = text.lower()

    has_urgency = int(any(k in lower for k in URGENCY_KEYWORDS))
    has_threat = int(any(k in lower for k in THREAT_KEYWORDS))
    has_kyc = int(any(k in lower for k in KYC_KEYWORDS))
    has_otp = int(any(k in lower for k in OTP_KEYWORDS))
    has_payment = int(any(k in lower for k in PAYMENT_REQUEST_KEYWORDS) or len(entities.get("upi_ids", [])) > 0)
    has_url = int(len(entities.get("urls", [])) > 0)
    has_sensitive = int(any(k in lower for k in SENSITIVE_INFO_KEYWORDS))
    has_reward = int(any(k in lower for k in REWARD_LURE_KEYWORDS))
    has_phone = int(len(entities.get("phone_numbers", [])) > 0)
    
    # Impersonation signals
    impersonation_keywords = ["police", "cbi", "cyber crime", "inspector", "customs", "manager", "ceo", "army", "officer", "hr"]
    has_impersonation = int(any(re.search(r'\b' + re.escape(k) + r'\b', lower) for k in impersonation_keywords))

    return {
        "urgency": has_urgency,
        "threat": has_threat,
        "kyc_request": has_kyc,
        "otp_request": has_otp,
        "payment_request": has_payment,
        "suspicious_url": has_url,
        "impersonation": has_impersonation,
        "credential_request": has_sensitive,
        "reward_lure": has_reward,
        "phone_contact": has_phone,
        "unknown_sender": 1 if (has_url or has_urgency or has_threat) else 0
    }
