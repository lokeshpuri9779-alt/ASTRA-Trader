from __future__ import annotations

from dataclasses import dataclass

from astra_trader.execution.reconciliation import PositionSnapshot, ReconciliationResult, reconcile_startup

@dataclass(frozen=True)
class UpstoxPositionRow:
    instrument_key: str
    quantity: int

def reconcile_upstox_positions(
    local_positions: dict[str,int],
    broker_rows: list[UpstoxPositionRow],
) -> ReconciliationResult:
    snapshots=[
        PositionSnapshot(symbol=r.instrument_key,quantity=int(r.quantity))
        for r in broker_rows
    ]
    return reconcile_startup(local_positions,snapshots)
