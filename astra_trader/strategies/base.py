from __future__ import annotations

from abc import ABC, abstractmethod
from astra_trader.core.events import Event
from astra_trader.models import TradeSignal

class Strategy(ABC):
    name: str = "base"

    @abstractmethod
    def on_event(self, event: Event) -> list[TradeSignal]:
        raise NotImplementedError
