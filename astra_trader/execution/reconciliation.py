from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class PositionSnapshot:
    symbol: str
    quantity: int

@dataclass(frozen=True)
class ReconciliationResult:
    ok: bool
    mismatches: tuple[str, ...]

def reconcile_startup(
    local_positions: dict[str, int],
    broker_positions: list[PositionSnapshot],
) -> ReconciliationResult:
    broker = {p.symbol: p.quantity for p in broker_positions}
    symbols = sorted(set(local_positions) | set(broker))
    mismatches = tuple(
        s for s in symbols
        if int(local_positions.get(s, 0)) != int(broker.get(s, 0))
    )
    return ReconciliationResult(ok=not mismatches, mismatches=mismatches)
