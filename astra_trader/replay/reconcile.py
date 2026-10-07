from __future__ import annotations

from dataclasses import dataclass

from .accounting import AccountLedger

@dataclass(frozen=True)
class Reconciliation:
    equity: float
    unrealized_pnl: float
    realized_pnl: float
    fees: float
    cash: float

def reconcile_ledger(ledger: AccountLedger, marks: dict[str, float]) -> Reconciliation:
    unrealized = 0.0
    for symbol, qty in ledger.positions.items():
        if qty == 0:
            continue
        mark = marks[symbol]
        avg = ledger.average_prices.get(symbol, 0.0)
        unrealized += qty * (mark - avg)
    return Reconciliation(
        equity=ledger.equity(marks),
        unrealized_pnl=unrealized,
        realized_pnl=ledger.realized_pnl,
        fees=ledger.fees,
        cash=ledger.cash,
    )
