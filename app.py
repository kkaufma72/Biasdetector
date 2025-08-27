"""Streamlit interface for the BiasBuster application."""

from __future__ import annotations

import tempfile

import pandas as pd
import streamlit as st

from bias_detection import BiasDetector
from diversity_predictor import DiversityPredictor
from llm_rewrite import rewrite_text
from spark_processor import analyze_dataset

st.set_page_config(page_title="BiasBuster", layout="wide")


def main() -> None:
    st.title("BiasBuster")
    st.write("Upload job descriptions or resumes to detect biased language, suggest neutral rewrites, and predict diversity impact.")

    detector = BiasDetector()
    predictor = DiversityPredictor()

    text_input = st.text_area("Paste text for analysis")
    file_input = st.file_uploader("...or upload a text file", type=["txt"])    

    if st.button("Analyze"):
        text = text_input
        if file_input is not None:
            text = file_input.read().decode("utf-8")
        if not text:
            st.warning("Please provide text or upload a file.")
            return

        biases = detector.find_biases(text)
        bias_count = sum(len(v) for v in biases.values())
        score_before = detector.neutrality_score(text)
        rewritten = rewrite_text(text)
        score_after = detector.neutrality_score(rewritten)

        st.subheader("Detected Biases")
        if biases:
            bias_df = pd.DataFrame([(k, len(v)) for k, v in biases.items()], columns=["category", "count"])
            st.bar_chart(bias_df.set_index("category"))
        else:
            st.write("No biases detected.")

        st.subheader("Suggested Rewrite")
        st.write(rewritten)

        st.subheader("Analytics")
        st.write(f"Neutrality score before: {score_before:.2%}")
        st.write(f"Neutrality score after: {score_after:.2%}")
        if score_before:
            improvement = (score_after - score_before) / score_before
            st.write(f"Bias reduction: {improvement*100:.1f}%")

        decrease = predictor.predict_decrease(bias_count)
        st.write(f"Predicted decrease in diverse applicants: {decrease:.1f}%")

    st.sidebar.header("Bulk Analysis")
    bulk = st.sidebar.file_uploader("Text file with one document per line", type=["txt"], key="bulk")
    if st.sidebar.button("Run Spark Analysis"):
        if bulk is None:
            st.sidebar.warning("Please upload a file for bulk processing.")
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
                tmp.write(bulk.read())
                tmp_path = tmp.name
            df = analyze_dataset(tmp_path)
            st.sidebar.write(df.toPandas())


if __name__ == "__main__":
    main()
