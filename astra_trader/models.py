from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class TradeAction(str, Enum):
    WAIT = "WAIT"
    ENTER = "ENTER"
    EXIT = "EXIT"
    REJECT = "REJECT"

@dataclass(frozen=True)
class TradeSignal:
    symbol: str
    side: str
    entry: float
    stop: float
    target_1: float
    target_2: float | None = None
    score: float = 0.0
    spread_pct: float = 0.0
    liquidity_ok: bool = True
    volatility_ok: bool = True
    metadata: dict = field(default_factory=dict)

@dataclass
class RiskState:
    starting_capital: float
    current_equity: float
    realized_pnl_today: float = 0.0
    losses_today: int = 0
    open_risk: float = 0.0
    kill_switch: bool = False
    updated_at: datetime = field(default_factory=datetime.utcnow)

@dataclass(frozen=True)
class RiskDecision:
    allowed: bool
    action: TradeAction
    quantity: int
    max_loss_rupees: float
    reason: str
