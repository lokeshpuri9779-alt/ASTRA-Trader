from __future__ import annotations

from collections import deque

from astra_trader.core.events import Event
from astra_trader.models import TradeSignal
from astra_trader.strategies.base import Strategy
from .utils import mean, stdev

class ZScoreMeanReversionStrategy(Strategy):
    name="zscore-mean-reversion-baseline"

    def __init__(self, lookback: int = 20, entry_z: float = 2.0):
        self.lookback=lookback
        self.entry_z=entry_z
        self.closes=deque(maxlen=lookback)

    def on_event(self,event: Event) -> list[TradeSignal]:
        close=float(event.payload["close"])
        symbol=str(event.payload["instrument_id"])
        self.closes.append(close)
        if len(self.closes)<self.lookback:
            return []
        hist=list(self.closes)
        m=mean(hist); s=stdev(hist)
        if s<=0:
            return []
        z=(close-m)/s
        if z <= -self.entry_z:
            stop=close-s
            return [TradeSignal(symbol,"BUY",close,stop,m,score=78)]
        if z >= self.entry_z:
            stop=close+s
            return [TradeSignal(symbol,"SELL",close,stop,m,score=78)]
        return []
