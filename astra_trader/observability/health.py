from dataclasses import dataclass
from enum import Enum

class HealthState(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNSAFE = "UNSAFE"
    UNKNOWN = "UNKNOWN"

@dataclass(frozen=True)
class HealthCheck:
    component: str
    state: HealthState
    message: str = ""
