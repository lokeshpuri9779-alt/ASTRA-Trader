from __future__ import annotations

from dataclasses import dataclass, field

@dataclass
class AccountLedger:
    cash: float
    realized_pnl: float = 0.0
    fees: float = 0.0
    positions: dict[str, int] = field(default_factory=dict)
    average_prices: dict[str, float] = field(default_factory=dict)

    def apply_fill(self, *, symbol: str, side: str, quantity: int, price: float, fee: float = 0.0) -> None:
        if quantity <= 0 or price < 0 or fee < 0:
            raise ValueError("Invalid fill.")
        signed = quantity if side.upper() == "BUY" else -quantity
        prev_qty = self.positions.get(symbol, 0)
        prev_avg = self.average_prices.get(symbol, 0.0)

        self.cash -= signed * price
        self.cash -= fee
        self.fees += fee

        new_qty = prev_qty + signed
        if prev_qty == 0 or (prev_qty > 0 and signed > 0) or (prev_qty < 0 and signed < 0):
            notional = abs(prev_qty) * prev_avg + quantity * price
            self.average_prices[symbol] = notional / abs(new_qty) if new_qty else 0.0
        else:
            closing_qty = min(abs(prev_qty), quantity)
            pnl_per_unit = (price - prev_avg) * (1 if prev_qty > 0 else -1)
            self.realized_pnl += closing_qty * pnl_per_unit
            if new_qty == 0:
                self.average_prices[symbol] = 0.0
            elif (prev_qty > 0 > new_qty) or (prev_qty < 0 < new_qty):
                self.average_prices[symbol] = price

        self.positions[symbol] = new_qty

    def equity(self, marks: dict[str, float]) -> float:
        unrealized = 0.0
        for symbol, qty in self.positions.items():
            if qty == 0:
                continue
            mark = marks[symbol]
            avg = self.average_prices.get(symbol, 0.0)
            unrealized += qty * (mark - avg)
        return self.cash + sum(q * marks.get(s, 0.0) for s, q in self.positions.items())


# Backward-compatible alias for earlier replay tests/API.
SimulationLedger = AccountLedger
