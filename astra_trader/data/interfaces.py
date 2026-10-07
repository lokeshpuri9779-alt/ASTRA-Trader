from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from astra_trader.core.events import Event

class MarketDataSource(ABC):
    @abstractmethod
    def stream(self) -> Iterable[Event]:
        raise NotImplementedError
