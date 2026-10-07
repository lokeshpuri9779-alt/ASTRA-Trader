from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Iterable

@dataclass(frozen=True)
class IndMoneyPosition:
    symbol: str
    quantity: float
    average_price: float | None = None
    current_price: float | None = None
    product: str | None = None
    underlying: str | None = None

@dataclass(frozen=True)
class IndMoneyMarketContext:
    symbol: str
    last_price: float | None = None
    implied_volatility: float | None = None
    open_interest: float | None = None
    delta: float | None = None
    gamma: float | None = None
    theta: float | None = None
    vega: float | None = None

class IndMoneyReadOnlyClient(Protocol):
    def positions(self) -> Iterable[IndMoneyPosition]:
        ...

    def market_context(self, symbols: list[str]) -> Iterable[IndMoneyMarketContext]:
        ...

class IndMoneyAdapter:
    """Read-only integration boundary.

    No order placement, funds transfer, profile mutation or account-setting methods
    are permitted in this interface.
    """

    def __init__(self, client: IndMoneyReadOnlyClient):
        self.client = client

    def fetch_positions(self) -> list[IndMoneyPosition]:
        return list(self.client.positions())

    def fetch_market_context(self, symbols: list[str]) -> list[IndMoneyMarketContext]:
        return list(self.client.market_context(symbols))
