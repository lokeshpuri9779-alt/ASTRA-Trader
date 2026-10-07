from dataclasses import dataclass

from astra_trader.core.modes import TradingMode
from astra_trader.paper import PaperBroker
from astra_trader.risk import RiskEngine

@dataclass
class AstraTrader:
    mode: TradingMode = TradingMode.PAPER

    def __post_init__(self) -> None:
        self.risk = RiskEngine()
        self.paper = PaperBroker()

    @property
    def live_enabled(self) -> bool:
        # Live broker execution is intentionally not wired in v1.
        return False
