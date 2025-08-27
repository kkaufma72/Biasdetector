"""Suggest neutral rewrites using a minimal rule-based approach."""

from typing import Dict

# Simple replacement dictionary. In a full implementation this would delegate to
# an LLM via OpenAI or Anthropic APIs.
REPLACEMENTS: Dict[str, str] = {
    "aggressive": "assertive",
    "dominant": "leading",
    "nurturing": "supportive",
    "urban": "inner-city",
    "ghetto": "under-resourced area",
}


def suggest_rewrite(text: str) -> str:
    """Return ``text`` with biased words replaced by neutral alternatives."""

    result = text
    for biased, neutral in REPLACEMENTS.items():
        result = result.replace(biased, neutral).replace(biased.title(), neutral.title())
    return result
