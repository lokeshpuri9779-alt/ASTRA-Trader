from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class RejectionPolicy:
    max_order_quantity: int | None = None
    reject_if_no_market: bool = True

    def check(
        self,
        *,
        quantity: int,
        has_market: bool,
        lot_size: int | None = None,
        available_cash: float | None = None,
        estimated_required_cash: float | None = None,
    ) -> str | None:
        if quantity <= 0:
            return "INVALID_QUANTITY"
        if self.max_order_quantity is not None and quantity > self.max_order_quantity:
            return "MAX_ORDER_QUANTITY"
        if lot_size and quantity % lot_size != 0:
            return "INVALID_LOT_SIZE"
        if self.reject_if_no_market and not has_market:
            return "NO_MARKET_DATA"
        if (
            available_cash is not None
            and estimated_required_cash is not None
            and estimated_required_cash > available_cash
        ):
            return "INSUFFICIENT_FUNDS"
        return None
