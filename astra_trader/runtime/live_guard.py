from __future__ import annotations

from astra_trader.runtime.environment import RuntimeConfig
from astra_trader.runtime.promotion import PromotionDecision

def assert_live_allowed(config: RuntimeConfig, promotion: PromotionDecision) -> None:
    if not config.live_enabled:
        raise RuntimeError("LIVE execution is disabled by configuration.")
    if not promotion.allowed:
        raise RuntimeError("LIVE promotion gate failed: " + ",".join(promotion.missing))
