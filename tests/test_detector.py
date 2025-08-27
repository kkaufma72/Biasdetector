import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from bias_detector.detector import find_biased_words


def test_find_biased_words():
    text = "We need an aggressive leader for our urban project."
    result = find_biased_words(text)
    assert "gender" in result and "aggressive" in result["gender"]
    assert "race" in result and "urban" in result["race"]
