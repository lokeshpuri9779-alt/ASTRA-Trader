from astra_trader.data.index_history import NseIndexHistoryLoader
from astra_trader.portfolio.limits import ExposureCaps, check_exposure_caps
from astra_trader.portfolio.liquidity import liquidity_position_cap
from astra_trader.portfolio.risk_budget import normalize_strategy_budgets
from astra_trader.portfolio.tail_risk import historical_var_cvar
from astra_trader.research.multiple_testing import deflated_sharpe

def test_multiple_testing_penalty():
    a=deflated_sharpe(observed_sharpe=1.5,trials=1,sample_size=252)
    b=deflated_sharpe(observed_sharpe=1.5,trials=100,sample_size=252)
    assert b.adjusted_threshold>a.adjusted_threshold

def test_portfolio_remaining_controls():
    ok=check_exposure_caps(
        total_equity=100000,
        proposed_underlying_exposure=20000,
        proposed_sector_exposure=20000,
        proposed_cluster_exposure=30000,
        caps=ExposureCaps(),
    )
    assert ok.allowed
    assert liquidity_position_cap(average_daily_volume=10000,participation_rate=.02,lot_size=50)==200
    budgets=normalize_strategy_budgets({"a":2,"b":1})
    assert round(budgets["a"],6)==round(2/3,6)
    tail=historical_var_cvar([-10,-5,1,2,3],alpha=.8)
    assert tail.cvar<=tail.var

def test_index_fixtures_load():
    loader=NseIndexHistoryLoader()
    _, bars=loader.load("test/fixtures/nifty_daily.csv",symbol="NIFTY 50")
    assert len(bars)==4
