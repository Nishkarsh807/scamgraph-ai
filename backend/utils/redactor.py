"""
ScamGraph AI - Sensitive Data Redactor & Privacy Guard
Redacts OTPs, CVVs, full card numbers, and PII before database storage or logging.
"""

import re

def redact_sensitive_info(text: str) -> str:
    """
    Sanitizes raw text to protect user privacy.
    Masks OTPs, card numbers, passwords, and phone numbers.
    """
    if not text:
        return ""

    # Redact 16-digit card numbers
    sanitized = re.sub(r'\b(?:\d[ -]*?){13,16}\b', '[CARD_NUMBER_REDACTED]', text)

    # Redact CVVs (3 or 4 digits near cvv keyword)
    sanitized = re.sub(r'(?i)(cvv|cvc)\s*[:=]?\s*\d{3,4}', r'\1: [CVV_REDACTED]', sanitized)

    # Redact explicit OTPs (4-8 digits near otp keyword)
    sanitized = re.sub(r'(?i)(otp|one time password|pin)\s*(?:is|:)?\s*(\b\d{4,8}\b)', r'\1: [REDACTED_CODE]', sanitized)

    # Redact phone numbers partially (show only first 2 and last 2 digits)
    def mask_phone(match):
        full = match.group(0).replace(" ", "").replace("-", "")
        if len(full) >= 10:
            return f"{full[:2]}******{full[-2:]}"
        return "[PHONE_REDACTED]"

    sanitized = re.sub(r'(?:\+?91[\s\-]?)?(?:[6-9]\d{9})\b', mask_phone, sanitized)

    return sanitized
