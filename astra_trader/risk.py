from dataclasses import dataclass
from .models import RiskDecision, RiskState, TradeAction, TradeSignal

@dataclass(frozen=True)
class RiskLimits:
    risk_per_trade_pct: float = 0.5
    max_daily_loss_pct: float = 2.0
    max_consecutive_losses: int = 3
    max_open_risk_pct: float = 1.5
    min_trade_score: float = 78.0
    max_spread_pct: float = 1.5
    max_position_value_pct: float = 20.0

class RiskEngine:
    def __init__(self, limits: RiskLimits | None = None):
        self.limits = limits or RiskLimits()

    def evaluate(self, signal: TradeSignal, state: RiskState) -> RiskDecision:
        if state.kill_switch:
            return self._reject("Kill switch is active.")
        if state.current_equity <= 0:
            return self._reject("Current equity must be positive.")
        daily_loss_limit = state.starting_capital * self.limits.max_daily_loss_pct / 100
        if state.realized_pnl_today <= -daily_loss_limit:
            return self._reject("Daily loss limit reached.")
        if state.losses_today >= self.limits.max_consecutive_losses:
            return self._reject("Maximum losing trades reached for the day.")
        if signal.score < self.limits.min_trade_score:
            return self._reject(f"Trade score {signal.score:.1f} is below threshold.")
        if not signal.liquidity_ok:
            return self._reject("Liquidity filter failed.")
        if not signal.volatility_ok:
            return self._reject("Volatility filter failed.")
        if signal.spread_pct > self.limits.max_spread_pct:
            return self._reject("Bid/ask spread is too wide.")
        per_unit_risk = abs(signal.entry - signal.stop)
        if per_unit_risk <= 0:
            return self._reject("Stop must differ from entry.")
        max_loss = state.current_equity * self.limits.risk_per_trade_pct / 100
        max_open_risk = state.current_equity * self.limits.max_open_risk_pct / 100
        available_risk = max(0.0, max_open_risk - state.open_risk)
        risk_budget = min(max_loss, available_risk)
        if risk_budget <= 0:
            return self._reject("No risk budget available.")
        quantity_by_risk = int(risk_budget // per_unit_risk)
        max_position_value = state.current_equity * self.limits.max_position_value_pct / 100
        quantity_by_value = int(max_position_value // signal.entry) if signal.entry > 0 else 0
        quantity = max(0, min(quantity_by_risk, quantity_by_value))
        if quantity < 1:
            return self._reject("Position size is below one unit at current risk limits.")
        return RiskDecision(True, TradeAction.ENTER, quantity, round(quantity * per_unit_risk, 2), "Passed deterministic ASTRA risk checks.")

    @staticmethod
    def _reject(reason: str) -> RiskDecision:
        return RiskDecision(False, TradeAction.REJECT, 0, 0.0, reason)
