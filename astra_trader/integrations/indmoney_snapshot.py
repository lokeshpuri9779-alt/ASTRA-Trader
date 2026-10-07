from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from astra_trader.integrations.indmoney import IndMoneyMarketContext, IndMoneyPosition

@dataclass(frozen=True)
class IndMoneySnapshot:
    captured_at: datetime
    positions: tuple[IndMoneyPosition, ...]
    market_context: tuple[IndMoneyMarketContext, ...]

    @property
    def symbols(self) -> tuple[str, ...]:
        return tuple(sorted({p.symbol for p in self.positions}))

def build_snapshot(
    *,
    captured_at: datetime,
    positions: list[IndMoneyPosition],
    market_context: list[IndMoneyMarketContext],
) -> IndMoneySnapshot:
    return IndMoneySnapshot(
        captured_at=captured_at,
        positions=tuple(positions),
        market_context=tuple(market_context),
    )
