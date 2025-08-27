"""Simple diversity impact predictor using Logistic Regression."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

logger = logging.getLogger(__name__)

MODEL_PATH = Path(__file__).parent / "models" / "diversity_model.pkl"
DATA_PATH = Path(__file__).parent / "data" / "sample_training.csv"


def train_model(data_path: Path = DATA_PATH, model_path: Path = MODEL_PATH) -> None:
    """Train and persist the logistic regression model."""
    df = pd.read_csv(data_path)
    X = df[["bias_count"]]
    y = df["low_diversity"]
    model = LogisticRegression()
    model.fit(X, y)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    logger.info("Model trained and saved to %s", model_path)


class DiversityPredictor:
    """Predict impact on diversity given a count of biased words."""

    def __init__(self, model_path: Optional[Path] = None) -> None:
        self.model_path = model_path or MODEL_PATH
        if not self.model_path.exists():
            train_model(model_path=self.model_path)
        self.model: LogisticRegression = joblib.load(self.model_path)

    def predict_decrease(self, bias_count: int) -> float:
        """Return predicted decrease in diverse applicants as a percentage."""
        proba = self.model.predict_proba(np.array([[bias_count]]))[0][1]
        return float(proba * 100)
