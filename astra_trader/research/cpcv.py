from __future__ import annotations

from itertools import combinations

def combinatorial_test_folds(n_blocks: int, test_blocks: int) -> list[tuple[int,...]]:
    if n_blocks <= 1 or test_blocks <= 0 or test_blocks >= n_blocks:
        raise ValueError("Invalid CPCV block configuration.")
    return list(combinations(range(n_blocks), test_blocks))

def block_ranges(n: int, n_blocks: int) -> list[tuple[int,int]]:
    if n_blocks <= 0 or n_blocks > n:
        raise ValueError("Invalid n_blocks.")
    base=n//n_blocks
    rem=n % n_blocks
    out=[]; start=0
    for i in range(n_blocks):
        size=base+(1 if i<rem else 0)
        out.append((start,start+size))
        start += size
    return out
