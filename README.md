# Bias Detector Web App

This project provides a simple demonstration of a bias detection tool for job
postings or resumes. It can:

* Identify potentially biased terms using a keyword list.
* Suggest neutral rewrites.
* Estimate impact on applicant diversity.

## Usage

Install dependencies and run the Streamlit app:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The implementation is a minimal prototype intended for extension. The bias
keyword lists and impact predictor are simple heuristics.
