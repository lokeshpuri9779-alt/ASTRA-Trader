from __future__ import annotations

def population_stability_index(expected: list[float], actual: list[float], epsilon: float=1e-9) -> float:
    if len(expected)!=len(actual) or not expected:
        raise ValueError("Expected and actual distributions must align.")
    total_e=sum(expected); total_a=sum(actual)
    if total_e<=0 or total_a<=0:
        raise ValueError("Distributions must have positive mass.")
    psi=0.0
    for e,a in zip(expected,actual):
        ep=max(e/total_e,epsilon)
        ap=max(a/total_a,epsilon)
        import math
        psi += (ap-ep)*math.log(ap/ep)
    return psi
