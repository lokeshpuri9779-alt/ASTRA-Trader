from __future__ import annotations

from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class CostBreakdown:
    brokerage: float = 0.0
    stt: float = 0.0
    exchange: float = 0.0
    sebi: float = 0.0
    gst: float = 0.0
    stamp: float = 0.0

    @property
    def total(self) -> float:
        return self.brokerage + self.stt + self.exchange + self.sebi + self.gst + self.stamp

class CostModel:
    """Versioned hook for India trading costs.

    Only STT rules explicitly encoded here are those effective from 2026-04-01.
    Other levies stay injectable/configurable rather than guessed.
    """

    def __init__(
        self,
        *,
        brokerage_flat: float = 0.0,
        exchange_rate: float = 0.0,
        sebi_rate: float = 0.0,
        gst_rate: float = 0.18,
        stamp_rate: float = 0.0,
    ):
        self.brokerage_flat = brokerage_flat
        self.exchange_rate = exchange_rate
        self.sebi_rate = sebi_rate
        self.gst_rate = gst_rate
        self.stamp_rate = stamp_rate

    def calculate(
        self,
        *,
        trade_date: date,
        segment: str,
        side: str,
        turnover: float,
        option_intrinsic_value: float = 0.0,
        exercised_option: bool = False,
    ) -> CostBreakdown:
        brokerage = self.brokerage_flat
        exchange = turnover * self.exchange_rate
        sebi = turnover * self.sebi_rate
        stamp = turnover * self.stamp_rate if side.upper() == "BUY" else 0.0

        stt = 0.0
        if trade_date >= date(2026, 4, 1):
            seg = segment.upper()
            if seg == "OPTION":
                if exercised_option:
                    stt = max(0.0, option_intrinsic_value) * 0.0015
                elif side.upper() == "SELL":
                    stt = turnover * 0.0015
            elif seg == "FUTURE" and side.upper() == "SELL":
                stt = turnover * 0.0005

        taxable = brokerage + exchange + sebi
        gst = taxable * self.gst_rate
        return CostBreakdown(
            brokerage=brokerage,
            stt=stt,
            exchange=exchange,
            sebi=sebi,
            gst=gst,
            stamp=stamp,
        )
