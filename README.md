# BiasBuster

BiasBuster is a demonstration web app for recruiters to detect biased language in job descriptions or resumes, suggest neutral rewrites using LLMs, and estimate the impact of bias on applicant diversity. The project includes Streamlit UI, basic analytics, a tiny ML model, and deployment assets for Docker and Kubernetes.

## Features
- Detect gender and race coded words using spaCy with a configurable dictionary.
- Rewrite text through LangChain + OpenAI (falls back to original text if no API key).
- Predict diversity impact with a logistic regression model trained on synthetic data.
- Analytics showing neutrality scores before/after rewrites and percentage improvement.
- PySpark helper for large batch processing.

- Dockerfile and Kubernetes manifests for scalable deployment.

## Running Locally
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm  # once
export OPENAI_API_KEY="sk-..."  # optional
streamlit run app.py
```

Upload text or a `.txt` file to analyze. The sidebar contains a PySpark demo for bulk processing.

## Re-training the Diversity Model
The logistic regression model is generated on first run and stored in
`models/diversity_model.pkl`. To regenerate it manually:
```bash
python -c "from diversity_predictor import train_model; train_model()"
```

## Docker
```bash
docker build -t biasbuster .
docker run -p 8501:8501 -e OPENAI_API_KEY=$OPENAI_API_KEY biasbuster
```

## Kubernetes
```bash
# push image to your registry then
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```
The service is configured as a `LoadBalancer`; modify as needed for your cluster.

## Cloud Storage & LLM Notes
The code is written to easily extend with AWS S3 (`boto3`) or GCP storage (`google-cloud-storage`). LangChain is used for LLM access; supply your OpenAI or Anthropic API key via environment variable.

## Security
Input text is sanitized and API keys are read from environment variables. For production, consider additional security such as request authentication and secret management.

## Disclaimer
The bias dictionary and prediction model are simplistic and intended for demonstration. Accuracy is limited; train on real, diverse datasets before using in production.
