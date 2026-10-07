from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import os

class RuntimeEnvironment(str, Enum):
    RESEARCH = "RESEARCH"
    PAPER = "PAPER"
    SHADOW = "SHADOW"
    LIVE = "LIVE"

@dataclass(frozen=True)
class RuntimeConfig:
    environment: RuntimeEnvironment
    live_enabled: bool

    @classmethod
    def from_env(cls) -> "RuntimeConfig":
        environment = RuntimeEnvironment(os.getenv("ASTRA_ENV","PAPER").upper())
        requested_live = os.getenv("ASTRA_LIVE_ENABLED","false").lower() == "true"
        live_enabled = environment is RuntimeEnvironment.LIVE and requested_live
        return cls(environment=environment, live_enabled=live_enabled)
