from __future__ import annotations

from dataclasses import dataclass

from astra_trader.observability.watchdog import watchdog_decision
from astra_trader.paper.divergence import compare_execution
from astra_trader.paper.shadow import ShadowGateway, ShadowIntent
from astra_trader.replay.accounting import AccountLedger
from astra_trader.runtime.promotion import PromotionDecision, PromotionEvidence, evaluate_live_promotion

@dataclass(frozen=True)
class IntegratedValidationResult:
    paper_ok: bool
    shadow_ok: bool
    reconciliation_ok: bool
    risk_ok: bool
    divergence_bps: float
    promotion: PromotionDecision

def run_integrated_validation(
    *,
    starting_cash: float = 100_000.0,
    symbol: str = "TEST",
    quantity: int = 10,
    replay_price: float = 100.0,
    shadow_price: float = 100.05,
    max_divergence_bps: float = 20.0,
) -> IntegratedValidationResult:
    ledger = AccountLedger(cash=starting_cash)
    ledger.apply_fill(symbol=symbol, side="BUY", quantity=quantity, price=replay_price)

    shadow = ShadowGateway()
    shadow.submit(ShadowIntent(symbol, "BUY", quantity, shadow_price))

    divergence = compare_execution(
        replay_price=replay_price,
        observed_shadow_price=shadow_price,
        replay_qty=quantity,
        shadow_qty=quantity,
        replay_pnl=0.0,
        shadow_pnl=0.0,
    )

    paper_ok = ledger.positions.get(symbol) == quantity
    shadow_ok = len(shadow.intents) == 1
    reconciliation_ok = abs(ledger.equity({symbol: replay_price}) - starting_cash) < 1e-9
    risk_ok = abs(divergence.fill_price_bps) <= max_divergence_bps

    watchdog = watchdog_decision(
        stale_data=False,
        reconciliation_ok=reconciliation_ok,
        component_healthy=paper_ok and shadow_ok and risk_ok,
    )

    promotion = evaluate_live_promotion(
        PromotionEvidence(
            ci_passed=True,
            secret_scan_passed=True,
            dependency_audit_passed=True,
            paper_validation_passed=paper_ok,
            shadow_validation_passed=shadow_ok,
            reconciliation_passed=reconciliation_ok,
            risk_checks_passed=(risk_ok and not watchdog.block_new_risk),
            compliance_verified=True,
            external_broker_ready=False,
        )
    )

    return IntegratedValidationResult(
        paper_ok=paper_ok,
        shadow_ok=shadow_ok,
        reconciliation_ok=reconciliation_ok,
        risk_ok=risk_ok,
        divergence_bps=divergence.fill_price_bps,
        promotion=promotion,
    )
