from __future__ import annotations

from astra_trader.integrations.indmoney_capabilities import OFFICIAL_INDMONEY_CAPABILITIES

def assert_indmoney_read_only() -> None:
    if not OFFICIAL_INDMONEY_CAPABILITIES.read_only:
        raise RuntimeError("INDmoney capability boundary violated.")

def assert_no_indmoney_execution() -> None:
    if OFFICIAL_INDMONEY_CAPABILITIES.order_write:
        raise RuntimeError("INDmoney execution is not permitted.")
