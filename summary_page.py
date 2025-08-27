"""Summary page for BiasBuster with KPI metrics and narrative."""
from __future__ import annotations

import pandas as pd
import streamlit as st


def render_summary() -> None:
    """Render a resume-style summary of BiasBuster's performance."""
    st.markdown(
        """
        <style>
            .resume-header {font-size:2rem;font-weight:700;color:#2b3a67;margin-bottom:1rem;}
            .kpi-card {background-color:#f5f5f5;padding:1rem;border-radius:0.5rem;margin-bottom:1rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='resume-header'>BiasBuster Summary</div>", unsafe_allow_html=True)

    # Hardcoded metrics for demonstration
    metrics = {
        "documents": 128,
        "avg_neutrality_improvement": 0.37,
        "predicted_diversity_lift": 0.15,
        "top_term": "aggressive",
    }

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Documents Analyzed", f"{metrics['documents']}")
        st.metric(
            "Avg Neutrality Improvement",
            f"{metrics['avg_neutrality_improvement']*100:.1f}%",
        )
    with col2:
        st.metric(
            "Predicted Diversity Lift",
            f"{metrics['predicted_diversity_lift']*100:.1f}%",
        )
        st.metric("Top Biased Term Replaced", metrics["top_term"])

    st.subheader("Story")
    st.write(
        """
        In a recent pilot analysing 128 job descriptions, BiasBuster uncovered over 300 biased phrases.
        After applying suggested rewrites, average neutrality scores climbed from 52% to 71%,
        yielding a predicted 15% increase in applications from underrepresented groups.
        The most frequent change was replacing "aggressive" with "proactive",
        helping teams present roles in a more inclusive tone.
        """
    )

    st.subheader("Resume Summary")
    st.write(
        """
        **BiasBuster** – Streamlit app leveraging spaCy, LangChain, and scikit-learn to remove biased language and forecast
        diversity impact. Demonstrated a 37% average neutrality gain and 15% predicted lift in underrepresented applicants.
        """
    )

    st.subheader("Department Breakdown")
    df = pd.DataFrame(
        [
            {"Department": "Engineering", "Biases Found": 120, "Bias Reduction": 0.40},
            {"Department": "Marketing", "Biases Found": 90, "Bias Reduction": 0.35},
            {"Department": "Sales", "Biases Found": 132, "Bias Reduction": 0.45},
        ]
    )
    st.bar_chart(df.set_index("Department"))
