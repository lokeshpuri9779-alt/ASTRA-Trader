from __future__ import annotations

from dataclasses import dataclass

from astra_trader.execution.upstox_credentials import check_upstox_credentials
from astra_trader.runtime.static_ip import validate_static_ips

@dataclass(frozen=True)
class UpstoxConnectionReadiness:
    credentials_ready: bool
    static_ip_ready: bool
    ready_for_auth: bool
    missing: tuple[str,...]

def evaluate_upstox_connection_readiness(
    *,
    primary_static_ip: str | None,
    secondary_static_ip: str | None = None,
) -> UpstoxConnectionReadiness:
    creds=check_upstox_credentials()
    ips=validate_static_ips(primary_static_ip,secondary_static_ip)
    missing=list(creds.missing)
    missing.extend(ips.errors)
    return UpstoxConnectionReadiness(
        credentials_ready=creds.configured,
        static_ip_ready=ips.ok,
        ready_for_auth=creds.configured and ips.ok,
        missing=tuple(missing),
    )
