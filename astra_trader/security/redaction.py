from __future__ import annotations

import re

_SENSITIVE_PATTERNS = [
    re.compile(r"(?i)(access[_-]?token|refresh[_-]?token|client[_-]?secret|api[_-]?key)\s*[:=]\s*([^\s,;]+)"),
    re.compile(r"(?i)(otp|mpin|password)\s*[:=]\s*([^\s,;]+)"),
]

def redact_sensitive(text: str) -> str:
    out = text
    for pattern in _SENSITIVE_PATTERNS:
        out = pattern.sub(lambda m: f"{m.group(1)}=[REDACTED]", out)
    return out
