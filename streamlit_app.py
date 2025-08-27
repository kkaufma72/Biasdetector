"""Streamlit interface for the bias detector."""

import streamlit as st
from bias_detector.detector import find_biased_words
from bias_detector.rewriter import suggest_rewrite
from bias_detector.predictor import predict_bias_impact

st.title("Bias Detector")

user_text = st.text_area("Job description or resume text")

if st.button("Analyze"):
    biases = find_biased_words(user_text)
    if not biases:
        st.success("No biased language detected.")
    else:
        st.write("Detected biases:", biases)
        rewritten = suggest_rewrite(user_text)
        st.write("Suggested rewrite:")
        st.write(rewritten)
        impact = predict_bias_impact(biases)
        st.write("Predicted impact on diversity (percentage points):", impact)
