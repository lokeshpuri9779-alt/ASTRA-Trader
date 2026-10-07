from datetime import date

from astra_trader.replay.costs import CostModel

def test_option_sell_stt_from_april_2026():
    model = CostModel()
    costs = model.calculate(
        trade_date=date(2026,4,1),
        segment="OPTION",
        side="SELL",
        turnover=100000,
    )
    assert costs.stt == 150.0

def test_future_sell_stt_from_april_2026():
    model = CostModel()
    costs = model.calculate(
        trade_date=date(2026,4,1),
        segment="FUTURE",
        side="SELL",
        turnover=100000,
    )
    assert costs.stt == 50.0
