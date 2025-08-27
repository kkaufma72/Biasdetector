"""Bias detection utilities using spaCy and a bias dictionary."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, List

import spacy

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

DEFAULT_DICT_PATH = Path(__file__).parent / "data" / "bias_dictionary.json"


class BiasDetector:
    """Detect biased words and compute neutrality scores."""

    def __init__(self, dict_path: str | None = None) -> None:
        self.dict_path = Path(dict_path) if dict_path else DEFAULT_DICT_PATH
        self.bias_dict = self._load_dict(self.dict_path)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning(
                "spaCy model 'en_core_web_sm' not found. Run `python -m spacy download en_core_web_sm`."
            )
            self.nlp = spacy.blank("en")

    @staticmethod
    def _load_dict(path: Path) -> Dict[str, List[str]]:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def find_biases(self, text: str) -> Dict[str, List[str]]:
        lower = text.lower()
        found: Dict[str, List[str]] = {}
        for category, words in self.bias_dict.items():
            matches = [w for w in words if w in lower]
            if matches:
                found[category] = matches
        return found

    def neutrality_score(self, text: str) -> float:
        doc = self.nlp(text)
        tokens = [t for t in doc if t.is_alpha]
        total = len(tokens)
        if total == 0:
            return 1.0
        biased_count = sum(len(v) for v in self.find_biases(text).values())
        return 1 - biased_count / total
