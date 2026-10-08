"""
ScamGraph AI - URL Threat & Heuristics Analyzer
Extracts domain, TLD, protocol, analyzes typosquatting, URL shorteners,
suspicious keywords, and produces an actionable URL risk score (0-100).
"""

import re
from urllib.parse import urlparse
from typing import Dict, Any, List

SUSPICIOUS_TLDS = {
    "xyz", "top", "live", "vip", "cc", "site", "apk", "biz", "pw",
    "rest", "online", "link", "info", "work", "tk", "ml", "ga", "cf", "gq"
}

KNOWN_SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "is.gd", "cutt.ly", "rb.gy",
    "shorturl.at", "ow.ly", "buff.ly", "rebrand.ly"
}

FINANCIAL_TARGET_BRANDS = [
    "sbi", "hdfc", "icici", "axis", "kotak", "pnb", "bob", "paytm",
    "phonepe", "gpay", "bhim", "cred", "incometax", "aadhaar", "epfo", "bses"
]

SUSPICIOUS_URL_KEYWORDS = [
    "kyc", "verify", "update", "login", "secure", "auth", "support", "helpdesk",
    "claim", "refund", "reward", "lottery", "mandate", "apk", "download", "portal"
]

IP_ADDRESS_PATTERN = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')


class URLAnalyzer:
    def analyze_url(self, raw_url: str) -> Dict[str, Any]:
        """
        Thoroughly analyzes a single URL and computes risk flags and score.
        """
        if not raw_url.startswith(("http://", "https://")):
            # Normalize for parsing
            parsed_url_str = "http://" + raw_url
        else:
            parsed_url_str = raw_url

        try:
            parsed = urlparse(parsed_url_str)
            hostname = parsed.hostname or ""
            path = parsed.path or ""
        except Exception:
            hostname = raw_url.split('/')[0]
            path = ""

        is_https = raw_url.startswith("https://")
        is_ip_address = bool(IP_ADDRESS_PATTERN.match(hostname))

        # Split host into subdomains and domain
        parts = hostname.split('.')
        tld = parts[-1].lower() if len(parts) > 1 else ""
        subdomains = parts[:-2] if len(parts) > 2 else []
        registered_domain = ".".join(parts[-2:]) if len(parts) >= 2 else hostname

        # Characteristics
        url_length = len(raw_url)
        is_shortener = hostname.lower() in KNOWN_SHORTENERS
        is_suspicious_tld = tld in SUSPICIOUS_TLDS
        excessive_subdomains = len(subdomains) >= 2

        # Brand impersonation detection in domain/path
        matched_brands = [b for b in FINANCIAL_TARGET_BRANDS if b in hostname.lower()]
        
        # Legitimate domain check
        legit_domains = {
            "onlinesbi.sbi", "sbi.co.in", "hdfcbank.com", "icicibank.com",
            "axisbank.com", "kotak.com", "pnbindia.in", "paytm.com",
            "phonepe.com", "google.com", "amazon.in", "incometax.gov.in"
        }
        is_whitelisted = registered_domain.lower() in legit_domains

        # Suspicious keywords
        found_keywords = [
            kw for kw in SUSPICIOUS_URL_KEYWORDS
            if kw in hostname.lower() or kw in path.lower()
        ]

        flags = []
        risk_points = 0

        if not is_https:
            flags.append("Insecure HTTP protocol")
            risk_points += 20

        if is_ip_address:
            flags.append("Direct IP address used instead of domain")
            risk_points += 40

        if is_shortener:
            flags.append("URL shortener obscures destination")
            risk_points += 30

        if is_suspicious_tld:
            flags.append(f"Uncommon / high-abuse TLD (.{tld})")
            risk_points += 25

        if excessive_subdomains:
            flags.append("Excessive subdomain nesting")
            risk_points += 15

        if matched_brands and not is_whitelisted:
            flags.append(f"Potential Brand Impersonation: {', '.join(matched_brands).upper()} in unverified host")
            risk_points += 45

        if found_keywords and not is_whitelisted:
            flags.append(f"Sensitive phishing keywords: {', '.join(found_keywords)}")
            risk_points += 20

        if url_length > 75:
            flags.append("Abnormally long URL length")
            risk_points += 10

        # If whitelisted domain with HTTPS
        if is_whitelisted and is_https:
            risk_score = 5.0
            flags = ["Verified official institution domain"]
        else:
            risk_score = min(100.0, float(risk_points))

        return {
            "url": raw_url,
            "hostname": hostname,
            "registered_domain": registered_domain,
            "tld": tld,
            "is_https": is_https,
            "is_shortener": is_shortener,
            "is_ip_address": is_ip_address,
            "is_suspicious_tld": is_suspicious_tld,
            "flags": flags,
            "risk_score": round(risk_score, 1),
            "is_suspicious": risk_score >= 40.0
        }

    def analyze_urls(self, urls: List[str]) -> Dict[str, Any]:
        """
        Analyzes a list of URLs and returns overall summary and individual reports.
        """
        if not urls:
            return {
                "has_urls": False,
                "url_risk_score": 0.0,
                "is_suspicious": False,
                "analyzed_urls": []
            }

        reports = [self.analyze_url(u) for u in urls]
        max_score = max(r["risk_score"] for r in reports)
        any_suspicious = any(r["is_suspicious"] for r in reports)

        return {
            "has_urls": True,
            "url_risk_score": max_score,
            "is_suspicious": any_suspicious,
            "analyzed_urls": reports
        }


url_analyzer = URLAnalyzer()
