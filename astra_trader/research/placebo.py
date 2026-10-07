from __future__ import annotations

import random

def permute_labels(values: list[float], seed: int=1) -> list[float]:
    out=list(values)
    random.Random(seed).shuffle(out)
    return out

def shuffled_trade_sequence(trades: list[float], seed: int=1) -> list[float]:
    out=list(trades)
    random.Random(seed).shuffle(out)
    return out
