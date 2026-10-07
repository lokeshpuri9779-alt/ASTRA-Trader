from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass(frozen=True)
class LatencyModel:
    market_data_ms: int = 0
    strategy_ms: int = 0
    risk_ms: int = 0
    broker_ms: int = 0

    def order_eligible_at(self, market_event_time: datetime) -> datetime:
        total = self.market_data_ms + self.strategy_ms + self.risk_ms + self.broker_ms
        return market_event_time + timedelta(milliseconds=total)
