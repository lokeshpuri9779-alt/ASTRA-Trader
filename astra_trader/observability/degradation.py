from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class StrategyHealth:
    state: str
    reason: str

def strategy_health(*, drawdown_pct: float, expected_drawdown_limit: float, expectancy: float) -> StrategyHealth:
    if abs(drawdown_pct) >= expected_drawdown_limit:
        return StrategyHealth("DISABLED","DRAWDOWN_LIMIT")
    if expectancy < 0:
        return StrategyHealth("WATCH","NEGATIVE_EXPECTANCY")
    return StrategyHealth("NORMAL","OK")
