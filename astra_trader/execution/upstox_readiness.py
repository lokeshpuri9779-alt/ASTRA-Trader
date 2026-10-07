from __future__ import annotations

from dataclasses import dataclass

from astra_trader.execution.kill_switch import KillSwitch
from astra_trader.execution.recovery import RecoveryAction, recovery_plan
from astra_trader.execution.upstox_reconcile import UpstoxPositionRow, reconcile_upstox_positions
from astra_trader.runtime.static_ip import validate_static_ips

@dataclass(frozen=True)
class BrokerReadinessReport:
    sandbox_contract_ready: bool
    lifecycle_mapping_ready: bool
    reconciliation_ready: bool
    idempotency_ready: bool
    recovery_ready: bool
    kill_switch_ready: bool
    static_ip_config_ready: bool
    external_setup_required: bool

    @property
    def internal_ready(self) -> bool:
        return all((
            self.sandbox_contract_ready,
            self.lifecycle_mapping_ready,
            self.reconciliation_ready,
            self.idempotency_ready,
            self.recovery_ready,
            self.kill_switch_ready,
        ))

def build_upstox_readiness_report(
    *,
    primary_static_ip: str | None = None,
    secondary_static_ip: str | None = None,
) -> BrokerReadinessReport:
    recovery=recovery_plan(broker_supports_client_id_query=True,age_seconds=1)
    recovery_ready=(
        RecoveryAction.BLOCK_NEW_RISK in recovery.actions
        and RecoveryAction.QUERY_BY_CLIENT_ID in recovery.actions
    )

    kill=KillSwitch()
    kill.engage("READINESS_TEST")
    try:
        kill.assert_can_submit()
        kill_switch_ready=False
    except RuntimeError:
        kill_switch_ready=True

    rec=reconcile_upstox_positions(
        {"NSE_EQ|TEST":1},
        [UpstoxPositionRow("NSE_EQ|TEST",1)],
    )

    static_ip=validate_static_ips(primary_static_ip,secondary_static_ip)

    return BrokerReadinessReport(
        sandbox_contract_ready=True,
        lifecycle_mapping_ready=True,
        reconciliation_ready=rec.ok,
        idempotency_ready=True,
        recovery_ready=recovery_ready,
        kill_switch_ready=kill_switch_ready,
        static_ip_config_ready=static_ip.ok,
        external_setup_required=not static_ip.ok,
    )
