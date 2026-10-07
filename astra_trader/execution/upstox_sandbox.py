from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class SandboxOrder:
    symbol: str
    side: str
    quantity: int
    order_type: str
    client_order_id: str

@dataclass(frozen=True)
class SandboxOrderResult:
    accepted: bool
    broker_order_id: str | None
    status: str
    message: str = ""

class UpstoxSandboxGateway(Protocol):
    """Contract for Upstox sandbox only. No live credentials or live orders."""

    def submit(self, order: SandboxOrder) -> SandboxOrderResult:
        ...

    def get_order(self, broker_order_id: str) -> SandboxOrderResult:
        ...

    def cancel(self, broker_order_id: str) -> SandboxOrderResult:
        ...
