from dataclasses import dataclass, field
from datetime import datetime
from .models import RiskDecision, TradeSignal

@dataclass
class PaperTrade:
    symbol: str
    side: str
    quantity: int
    entry: float
    stop: float
    target_1: float
    target_2: float | None
    opened_at: datetime = field(default_factory=datetime.utcnow)
    status: str = "OPEN"

class PaperBroker:
    """No network calls, no broker credentials, no real orders."""
    def __init__(self):
        self.trades: list[PaperTrade] = []

    def place(self, signal: TradeSignal, decision: RiskDecision) -> PaperTrade:
        if not decision.allowed or decision.quantity <= 0:
            raise ValueError(f"Trade rejected: {decision.reason}")
        trade = PaperTrade(signal.symbol, signal.side, decision.quantity, signal.entry, signal.stop, signal.target_1, signal.target_2)
        self.trades.append(trade)
        return trade
