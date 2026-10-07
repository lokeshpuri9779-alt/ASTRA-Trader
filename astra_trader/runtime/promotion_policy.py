from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class ProductionPromotionEvidence:
    integrated_validation_passed: bool
    broker_reconciliation_passed: bool
    kill_switch_tested: bool
    unknown_submission_recovery_tested: bool
    static_ip_verified: bool
    credentials_loaded_securely: bool
    limited_live_completed: bool
    zero_unresolved_incidents: bool
    explicit_user_authorization: bool

@dataclass(frozen=True)
class ProductionPromotionDecision:
    allowed: bool
    missing: tuple[str, ...]

def evaluate_production_promotion(e: ProductionPromotionEvidence) -> ProductionPromotionDecision:
    checks = {
        "INTEGRATED_VALIDATION": e.integrated_validation_passed,
        "BROKER_RECONCILIATION": e.broker_reconciliation_passed,
        "KILL_SWITCH": e.kill_switch_tested,
        "UNKNOWN_SUBMISSION_RECOVERY": e.unknown_submission_recovery_tested,
        "STATIC_IP": e.static_ip_verified,
        "SECURE_CREDENTIALS": e.credentials_loaded_securely,
        "LIMITED_LIVE": e.limited_live_completed,
        "NO_UNRESOLVED_INCIDENTS": e.zero_unresolved_incidents,
        "USER_AUTHORIZATION": e.explicit_user_authorization,
    }
    missing=tuple(k for k,v in checks.items() if not v)
    return ProductionPromotionDecision(allowed=not missing, missing=missing)
