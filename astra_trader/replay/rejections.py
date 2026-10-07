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


    def evaluate(
        self,
        *,
        quantity: int,
        lot_size: int | None,
        has_market_data: bool,
        available_cash: float | None = None,
        required_cash: float | None = None,
    ) -> str | None:
        result = self.check(
            quantity=quantity,
            has_market=has_market_data,
            lot_size=lot_size,
            available_cash=available_cash,
            estimated_required_cash=required_cash,
        )
        aliases = {
            "MAX_ORDER_QUANTITY": "MAX_ORDER_QUANTITY_EXCEEDED",
            "NO_MARKET_DATA": "MISSING_MARKET_DATA",
            "INSUFFICIENT_FUNDS": "INSUFFICIENT_CASH",
        }
        return aliases.get(result, result)
