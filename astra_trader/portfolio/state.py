from dataclasses import dataclass, field

@dataclass
class Position:
    instrument: str
    quantity: int = 0
    average_price: float = 0.0
    unrealized_pnl: float = 0.0
    realized_pnl: float = 0.0

@dataclass
class PortfolioState:
    cash: float
    equity: float
    gross_exposure: float = 0.0
    net_exposure: float = 0.0
    open_risk: float = 0.0
    positions: dict[str, Position] = field(default_factory=dict)
