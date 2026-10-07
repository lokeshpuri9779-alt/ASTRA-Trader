from __future__ import annotations

from astra_trader.integrations.indmoney import IndMoneyPosition
from astra_trader.portfolio.state import PortfolioState, Position

def normalize_positions(
    positions: list[IndMoneyPosition],
    *,
    cash: float = 0.0,
) -> PortfolioState:
    mapped: dict[str, Position] = {}
    gross = 0.0
    net = 0.0

    for p in positions:
        price = float(p.current_price or p.average_price or 0.0)
        qty = int(p.quantity)
        notional = qty * price
        gross += abs(notional)
        net += notional
        mapped[p.symbol] = Position(
            instrument=p.symbol,
            quantity=qty,
            average_price=float(p.average_price or 0.0),
        )

    equity = cash + net
    return PortfolioState(
        cash=cash,
        equity=equity,
        gross_exposure=gross,
        net_exposure=net,
        positions=mapped,
    )
