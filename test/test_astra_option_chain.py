from datetime import datetime

from astra_trader.data.option_chain import OptionObservation

def test_option_spread_metrics():
    obs = OptionObservation(
        option_instrument_id="OPT1",
        underlying_instrument_id="NIFTY",
        timestamp=datetime(2026,10,8),
        underlying_price=25000,
        expiry="2026-10-08",
        strike=25000,
        option_type="CE",
        bid=99,
        ask=101,
    )
    assert obs.spread == 2
    assert round(obs.spread_pct, 6) == 2.0
