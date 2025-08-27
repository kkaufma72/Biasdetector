"""Detect biased language in text using simple keyword lists."""

from typing import List, Dict

# Simple keyword dictionary. In a production system, this could be replaced with
# a model or a more comprehensive dataset.
BIAS_KEYWORDS: Dict[str, List[str]] = {
    "gender": [
        "aggressive",
        "dominant",
        "nurturing",
    ],
    "race": [
        "urban",
        "ghetto",
    ],
}


def find_biased_words(text: str) -> Dict[str, List[str]]:
    """Return biased words grouped by category found in ``text``.

    The function performs a case-insensitive search for words defined in
    :data:`BIAS_KEYWORDS` and returns a dictionary mapping the bias category to
    a list of matched words.
    """

    lower = text.lower()
    found: Dict[str, List[str]] = {}
    for category, words in BIAS_KEYWORDS.items():
        matches = [w for w in words if w in lower]
        if matches:
            found[category] = matches
    return found
