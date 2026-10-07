from astra_trader.features.options import iv_minus_realized, skew_difference, term_structure
from astra_trader.regime.expiry import classify_expiry_regime
from astra_trader.research.cpcv import block_ranges, combinatorial_test_folds
from astra_trader.research.sweeps import parameter_grid, robustness_neighbors
from astra_trader.strategies.momentum import relative_strength_rank
from astra_trader.strategies.volatility import volatility_expansion

def test_research_helpers():
    assert len(parameter_grid({"a":[1,2],"b":[3,4]}))==4
    assert len(robustness_neighbors({"x":10},.1))==3
    assert combinatorial_test_folds(4,2)
    assert block_ranges(10,3)[-1][1]==10

def test_strategy_features():
    assert relative_strength_rank({"A":.2,"B":.1})[0][0]=="A"
    assert volatility_expansion(3,[1,1,1],2)
    assert iv_minus_realized(implied_vol=20,realized_vol=15)==5
    assert term_structure(15,18)==3
    assert skew_difference(22,18)==4
    r=classify_expiry_regime(days_to_expiry=0,abs_gamma=.2,gamma_threshold=.1)
    assert r.is_expiry_day and r.gamma_sensitive
