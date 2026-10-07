from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class IndMoneyCapabilities:
    portfolio_read: bool = True
    live_positions_read: bool = True
    market_data_read: bool = True
    option_chain_read: bool = True
    greeks_read: bool = True
    watchlist_read: bool = True
    order_write: bool = False
    transfer_write: bool = False
    account_settings_write: bool = False

    @property
    def read_only(self) -> bool:
        return not any((
            self.order_write,
            self.transfer_write,
            self.account_settings_write,
        ))

OFFICIAL_INDMONEY_CAPABILITIES = IndMoneyCapabilities()
