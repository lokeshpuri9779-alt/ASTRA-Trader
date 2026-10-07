from __future__ import annotations

from dataclasses import dataclass

from .accounting import SimulationLedger

@dataclass(frozen=True)
class Reconciliation:
    equity: float
    unrealized_pnl: float
    realized_pnl: float
    fees: float
    cash: float

def reconcile_ledger(ledger: SimulationLedger, marks: dict[str, float]) -> Reconciliation:
    equity, unrealized = ledger.mark_to_market(marks)
    realized = sum(p.realized_pnl for p in ledger.positions.values())
    return Reconciliation(
        equity=equity,
        unrealized_pnl=unrealized,
        realized_pnl=realized,
        fees=ledger.fees,
        cash=float(ledger.cash),
    )
