from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Iterable

@dataclass(frozen=True)
class BrokerPosition:
    instrument_key: str
    quantity: int

@dataclass(frozen=True)
class BrokerOrderSnapshot:
    order_id: str
    client_order_id: str | None
    status: str
    instrument_key: str
    quantity: int

class UpstoxReadOnlyGateway(Protocol):
    """Read-only contract for pre-live reconciliation and monitoring."""

    def positions(self) -> Iterable[BrokerPosition]:
        ...

    def orders(self) -> Iterable[BrokerOrderSnapshot]:
        ...

    def holdings(self) -> Iterable[dict]:
        ...

    def funds(self) -> dict:
        ...

# Deliberately no order-placement method here.
