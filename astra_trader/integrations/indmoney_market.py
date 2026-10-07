from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from astra_trader.integrations.indmoney import IndMoneyMarketContext

@dataclass(frozen=True)
class NormalizedMarketContext:
    symbol: str
    timestamp: datetime
    last_price: float | None
    implied_volatility: float | None
    open_interest: float | None
    delta: float | None
    gamma: float | None
    theta: float | None
    vega: float | None
    source: str = "INDMONEY_READ_ONLY"

def normalize_market_context(
    rows: list[IndMoneyMarketContext],
    *,
    timestamp: datetime,
) -> list[NormalizedMarketContext]:
    return [
        NormalizedMarketContext(
            symbol=r.symbol,
            timestamp=timestamp,
            last_price=r.last_price,
            implied_volatility=r.implied_volatility,
            open_interest=r.open_interest,
            delta=r.delta,
            gamma=r.gamma,
            theta=r.theta,
            vega=r.vega,
        )
        for r in rows
    ]
