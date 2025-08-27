"""Heuristic bias impact predictor."""

from typing import Dict


def predict_bias_impact(biases: Dict[str, list]) -> Dict[str, float]:
    """Return a naive estimate of diversity impact.

    The prediction is purely demonstrative: each biased word reduces the
    predicted representation of the affected group by 5%.
    """

    impact = {}
    for category, words in biases.items():
        impact[category] = -5.0 * len(words)
    return impact
