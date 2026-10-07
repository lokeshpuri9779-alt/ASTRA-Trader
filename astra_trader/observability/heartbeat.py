from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass(frozen=True)
class Heartbeat:
    component: str
    timestamp: datetime

def is_stale(heartbeat: Heartbeat, *, now: datetime, max_age: timedelta) -> bool:
    return now - heartbeat.timestamp > max_age
