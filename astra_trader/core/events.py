from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
import uuid

class EventType(str, Enum):
    MARKET_DATA = "MARKET_DATA"
    FEATURE = "FEATURE"
    SIGNAL = "SIGNAL"
    RISK = "RISK"
    ORDER_INTENT = "ORDER_INTENT"
    ORDER_UPDATE = "ORDER_UPDATE"
    FILL = "FILL"
    PORTFOLIO = "PORTFOLIO"
    HEALTH = "HEALTH"

@dataclass(frozen=True)
class Event:
    event_type: EventType
    event_time: datetime
    received_at: datetime
    payload: dict[str, Any]
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
