from __future__ import annotations

from collections import deque

from astra_trader.core.events import Event
from astra_trader.models import TradeSignal
from astra_trader.strategies.base import Strategy

class TrendBreakoutStrategy(Strategy):
    name="trend-breakout-baseline"

    def __init__(self, lookback: int = 20, threshold: float = 0.01):
        self.lookback=lookback
        self.threshold=threshold
        self.closes=deque(maxlen=lookback+1)

    def on_event(self,event: Event) -> list[TradeSignal]:
        close=float(event.payload["close"])
        symbol=str(event.payload["instrument_id"])
        self.closes.append(close)
        if len(self.closes)<self.lookback+1:
            return []
        history=list(self.closes)[:-1]
        high=max(history)
        low=min(history)
        if close > high*(1+self.threshold):
            return [TradeSignal(symbol,"BUY",close,low,close+(close-low),score=80)]
        if close < low*(1-self.threshold):
            return [TradeSignal(symbol,"SELL",close,high,close-(high-close),score=80)]
        return []
