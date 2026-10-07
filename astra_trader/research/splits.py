from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class TimeSplit:
    train_start: int
    train_end: int
    test_start: int
    test_end: int

def chronological_split(n: int, train_fraction: float = 0.7) -> TimeSplit:
    if n < 2:
        raise ValueError("Need at least two observations.")
    cut = max(1, min(n - 1, int(n * train_fraction)))
    return TimeSplit(0, cut, cut, n)

def walk_forward_splits(n: int, train_size: int, test_size: int, step: int | None = None) -> list[TimeSplit]:
    if train_size <= 0 or test_size <= 0:
        raise ValueError("train_size and test_size must be positive.")
    step = step or test_size
    out=[]
    start=0
    while start + train_size + test_size <= n:
        out.append(TimeSplit(start,start+train_size,start+train_size,start+train_size+test_size))
        start += step
    return out

def purged_split(split: TimeSplit, purge: int = 0, embargo: int = 0) -> TimeSplit:
    train_end=max(split.train_start, split.train_end-purge)
    test_start=min(split.test_end, split.test_start+embargo)
    return TimeSplit(split.train_start,train_end,test_start,split.test_end)
