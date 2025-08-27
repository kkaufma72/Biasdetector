"""PySpark helpers for processing large batches of text."""

from __future__ import annotations

from typing import Optional

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType

from bias_detection import BiasDetector


def analyze_dataset(path: str, spark: Optional[SparkSession] = None) -> DataFrame:
    """Return a DataFrame with bias counts for each line in ``path``."""
    spark = spark or SparkSession.builder.appName("biasbuster").getOrCreate()
    detector = BiasDetector()

    def count_bias(text: str) -> int:
        return sum(len(v) for v in detector.find_biases(text).values())

    bias_udf = udf(count_bias, IntegerType())
    df = spark.read.text(path).withColumn("bias_count", bias_udf("value"))
    return df
