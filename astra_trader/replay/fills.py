from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

@dataclass(frozen=True)
class MarketSnapshot:
    bid: float | None = None
    ask: float | None = None
    last: float | None = None
    volume: float | None = None

@dataclass(frozen=True)
class Fill:
    quantity: int
    price: float
    slippage: float
    partial: bool

@dataclass(frozen=True)
class FillModel:
    max_volume_participation: float = 0.10
    slippage_bps: float = 0.0

    def market_fill(self, *, side: Side, quantity: int, snapshot: MarketSnapshot) -> Fill | None:
        if quantity <= 0:
            return None

        reference = snapshot.ask if side is Side.BUY else snapshot.bid
        if reference is None:
            reference = snapshot.last
        if reference is None or reference <= 0:
            return None

        fill_qty = quantity
        if snapshot.volume is not None and snapshot.volume >= 0:
            cap = int(snapshot.volume * self.max_volume_participation)
            if cap <= 0:
                return None
            fill_qty = min(quantity, cap)

        direction = 1 if side is Side.BUY else -1
        slip = reference * (self.slippage_bps / 10000.0) * direction
        price = reference + slip
        return Fill(
            quantity=fill_qty,
            price=price,
            slippage=abs(slip),
            partial=fill_qty < quantity,
        )
