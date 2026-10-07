from __future__ import annotations

from dataclasses import dataclass

from astra_trader.integrations.indmoney import IndMoneyPosition
from astra_trader.portfolio.state import PortfolioState

@dataclass(frozen=True)
class IndMoneyReconciliation:
    ok: bool
    mismatches: tuple[str, ...]

def reconcile_indmoney_positions(
    portfolio: PortfolioState,
    remote_positions: list[IndMoneyPosition],
) -> IndMoneyReconciliation:
    remote = {p.symbol: int(p.quantity) for p in remote_positions}
    local = {s: int(p.quantity) for s,p in portfolio.positions.items()}
    symbols = sorted(set(local) | set(remote))
    mismatches = tuple(
        s for s in symbols if local.get(s,0) != remote.get(s,0)
    )
    return IndMoneyReconciliation(ok=not mismatches, mismatches=mismatches)
