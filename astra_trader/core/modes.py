from enum import Enum

class TradingMode(str, Enum):
    RESEARCH = "RESEARCH"
    PAPER = "PAPER"
    SHADOW = "SHADOW"
    LIVE = "LIVE"

DEFAULT_MODE = TradingMode.PAPER
