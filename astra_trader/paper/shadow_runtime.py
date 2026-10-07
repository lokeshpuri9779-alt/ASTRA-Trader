from __future__ import annotations

from dataclasses import dataclass

from astra_trader.integrations.indmoney_snapshot import IndMoneySnapshot
from astra_trader.paper.shadow import ShadowGateway, ShadowIntent

@dataclass(frozen=True)
class ShadowAssessment:
    symbol: str
    reference_price: float
    action: str
    reason: str

@dataclass(frozen=True)
class ShadowRunResult:
    assessments: tuple[ShadowAssessment, ...]
    hypothetical_orders: int

class IndMoneyShadowRuntime:
    """Consumes read-only INDmoney snapshots and emits hypothetical intents only."""

    def __init__(self, gateway: ShadowGateway | None = None):
        self.gateway = gateway or ShadowGateway()

    def assess(self, snapshot: IndMoneySnapshot) -> ShadowRunResult:
        context = {m.symbol: m for m in snapshot.market_context}
        assessments: list[ShadowAssessment] = []

        for position in snapshot.positions:
            row = context.get(position.symbol)
            price = float(
                (row.last_price if row and row.last_price is not None else None)
                or position.current_price
                or position.average_price
                or 0.0
            )
            if price <= 0:
                assessments.append(
                    ShadowAssessment(position.symbol, price, "WAIT", "NO_VALID_PRICE")
                )
                continue

            assessments.append(
                ShadowAssessment(position.symbol, price, "MONITOR", "READ_ONLY_POSITION_CONTEXT")
            )

        return ShadowRunResult(
            assessments=tuple(assessments),
            hypothetical_orders=len(self.gateway.intents),
        )

    def record_hypothetical(
        self,
        *,
        symbol: str,
        side: str,
        quantity: int,
        reference_price: float,
        metadata: dict | None = None,
    ) -> None:
        self.gateway.submit(
            ShadowIntent(
                symbol=symbol,
                side=side,
                quantity=quantity,
                reference_price=reference_price,
                metadata=metadata or {"source": "INDMONEY_READ_ONLY"},
            )
        )
