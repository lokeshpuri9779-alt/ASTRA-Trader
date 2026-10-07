from astra_trader.research.hypothesis import Hypothesis
from astra_trader.research.monte_carlo import resample_trade_pnls
from astra_trader.research.runner import run_candidate
from astra_trader.research.splits import chronological_split, walk_forward_splits, purged_split

def test_splits():
    s=chronological_split(100,0.7)
    assert s.train_end==70 and s.test_start==70
    wf=walk_forward_splits(100,60,20,20)
    assert len(wf)==2
    p=purged_split(wf[0],purge=2,embargo=1)
    assert p.train_end==58 and p.test_start==61

def test_monte_carlo():
    m=resample_trade_pnls([1,-1,2,-0.5],runs=50,seed=1)
    assert m.worst_final_pnl <= m.best_final_pnl

def test_research_runner():
    h=Hypothesis("h1","demo","NIFTY","1d",{},{"min_profit_factor":1.0},100)
    r=run_candidate(h,parameters={},evaluator=lambda p:[1,-0.5,1,-0.5])
    assert r.passed
