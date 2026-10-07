from astra_trader.scoring import SignalInputs, score_signal

def test_score_is_bounded_and_weighted():
    score = score_signal(
        SignalInputs(
            trend=100,
            volume=100,
            vwap_alignment=100,
            oi_alignment=100,
            pcr_alignment=100,
            iv_quality=100,
            greek_quality=100,
            liquidity=100,
        )
    )
    assert score == 100.0

def test_score_clamps_inputs():
    score = score_signal(
        SignalInputs(
            trend=200,
            volume=-10,
            vwap_alignment=50,
            oi_alignment=50,
            pcr_alignment=50,
            iv_quality=50,
            greek_quality=50,
            liquidity=50,
        )
    )
    assert 0.0 <= score <= 100.0
