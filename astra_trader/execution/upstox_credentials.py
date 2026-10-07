from __future__ import annotations

from dataclasses import dataclass
import os

@dataclass(frozen=True)
class UpstoxCredentialStatus:
    configured: bool
    missing: tuple[str, ...]

REQUIRED_UPSTOX_ENV = (
    "UPSTOX_CLIENT_ID",
    "UPSTOX_CLIENT_SECRET",
    "UPSTOX_REDIRECT_URI",
)

def check_upstox_credentials() -> UpstoxCredentialStatus:
    missing=tuple(name for name in REQUIRED_UPSTOX_ENV if not os.getenv(name))
    return UpstoxCredentialStatus(configured=not missing,missing=missing)
