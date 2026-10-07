from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterable

from astra_trader.core.events import Event, EventType
from astra_trader.models import RiskState
from astra_trader.portfolio.state import PortfolioState
from astra_trader.risk import RiskEngine
from astra_trader.strategies.base import Strategy

@dataclass
class ReplayResult:
    events_processed: int = 0
    signals_generated: int = 0
    signals_allowed: int = 0
    signals_rejected: int = 0

class ReplayEngine:
    """Deterministic event replay.

    The engine processes input events strictly in ascending event_time order.
    It does not submit live orders.
    """

    def __init__(self, strategy: Strategy, risk: RiskEngine | None = None):
        self.strategy = strategy
        self.risk = risk or RiskEngine()

    def run(
        self,
        events: Iterable[Event],
        portfolio: PortfolioState,
        risk_state: RiskState,
    ) -> ReplayResult:
        ordered = sorted(events, key=lambda e: (e.event_time, e.received_at, e.event_id))
        result = ReplayResult()

        last_event_time = None
        for event in ordered:
            if last_event_time is not None and event.event_time < last_event_time:
                raise ValueError("Replay event ordering violation.")
            last_event_time = event.event_time
            result.events_processed += 1

            if event.event_type is not EventType.MARKET_DATA:
                continue

            signals = self.strategy.on_event(event)
            result.signals_generated += len(signals)

            for signal in signals:
                decision = self.risk.evaluate(signal, risk_state)
                if decision.allowed:
                    result.signals_allowed += 1
                else:
                    result.signals_rejected += 1

        return result
