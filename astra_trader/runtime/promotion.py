from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class PromotionEvidence:
    ci_passed: bool
    secret_scan_passed: bool
    dependency_audit_passed: bool
    paper_validation_passed: bool
    shadow_validation_passed: bool
    reconciliation_passed: bool
    risk_checks_passed: bool
    compliance_verified: bool
    external_broker_ready: bool

@dataclass(frozen=True)
class PromotionDecision:
    allowed: bool
    missing: tuple[str, ...]

def evaluate_live_promotion(e: PromotionEvidence) -> PromotionDecision:
    checks = {
        "CI": e.ci_passed,
        "SECRET_SCAN": e.secret_scan_passed,
        "DEPENDENCY_AUDIT": e.dependency_audit_passed,
        "PAPER_VALIDATION": e.paper_validation_passed,
        "SHADOW_VALIDATION": e.shadow_validation_passed,
        "RECONCILIATION": e.reconciliation_passed,
        "RISK_CHECKS": e.risk_checks_passed,
        "COMPLIANCE": e.compliance_verified,
        "BROKER_READY": e.external_broker_ready,
    }
    missing=tuple(k for k,v in checks.items() if not v)
    return PromotionDecision(allowed=not missing, missing=missing)
