from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class RegimeCluster:
    label: int
    mean_return: float
    volatility: float

def cluster_regime_features(features: list[tuple[float,float]], k: int = 2) -> list[int]:
    """Research-only deterministic k-means-lite challenger.

    This deliberately avoids any live self-learning or execution linkage.
    """
    if k < 2 or len(features) < k:
        raise ValueError("Need at least k observations and k>=2.")
    centers = list(features[:k])
    labels = [0] * len(features)

    for _ in range(20):
        changed = False
        for i, x in enumerate(features):
            best = min(
                range(k),
                key=lambda j: (x[0]-centers[j][0])**2 + (x[1]-centers[j][1])**2,
            )
            if labels[i] != best:
                labels[i] = best
                changed = True
        new_centers = []
        for j in range(k):
            members = [features[i] for i,l in enumerate(labels) if l == j]
            if not members:
                new_centers.append(centers[j])
            else:
                new_centers.append((
                    sum(x[0] for x in members)/len(members),
                    sum(x[1] for x in members)/len(members),
                ))
        centers = new_centers
        if not changed:
            break
    return labels
