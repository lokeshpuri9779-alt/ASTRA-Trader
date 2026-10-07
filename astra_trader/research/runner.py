from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .diagnostics import Diagnostics, summarize
from .hypothesis import Hypothesis

@dataclass(frozen=True)
class ResearchRun:
    hypothesis_id: str
    parameters: dict
    diagnostics: Diagnostics
    passed: bool

def run_candidate(
    hypothesis: Hypothesis,
    *,
    parameters: dict,
    evaluator: Callable[[dict], list[float]],
) -> ResearchRun:
    returns=evaluator(parameters)
    diagnostics=summarize(returns)
    criteria=hypothesis.pass_criteria
    passed=True
    if "min_sharpe" in criteria:
        passed &= diagnostics.sharpe >= criteria["min_sharpe"]
    if "max_drawdown_abs" in criteria:
        passed &= abs(diagnostics.max_drawdown) <= criteria["max_drawdown_abs"]
    if "min_profit_factor" in criteria:
        passed &= diagnostics.profit_factor >= criteria["min_profit_factor"]
    return ResearchRun(hypothesis.hypothesis_id,dict(parameters),diagnostics,bool(passed))
