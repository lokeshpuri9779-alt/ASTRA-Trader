from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class WatchdogDecision:
    block_new_risk: bool
    disable_component: str | None
    reason: str

def watchdog_decision(*, stale_data: bool, reconciliation_ok: bool, component_healthy: bool) -> WatchdogDecision:
    if not reconciliation_ok:
        return WatchdogDecision(True,None,"RECONCILIATION_MISMATCH")
    if stale_data:
        return WatchdogDecision(True,None,"STALE_DATA")
    if not component_healthy:
        return WatchdogDecision(True,"strategy","COMPONENT_UNHEALTHY")
    return WatchdogDecision(False,None,"OK")
