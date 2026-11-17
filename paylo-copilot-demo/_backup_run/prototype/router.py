"""Step 1 — the router (rung 2: classical ML). A baseline is provided: run it, look at the confusions, improve if you have time, commit."""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

MODEL = None


def train(csv_path="data/tickets_synthetic.csv"):
    """Train TF-IDF + logistic regression on text -> category. Return the fitted pipeline."""
    global MODEL
    df = pd.read_csv(csv_path)
    MODEL = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), min_df=1), LogisticRegression(max_iter=1000))
    MODEL.fit(df["text"], df["category"])
    return MODEL


def predict(text):
    """Return (category, confidence). Confidence = max predict_proba."""
    if MODEL is None:
        train()
    proba = MODEL.predict_proba([text])[0]
    i = proba.argmax()
    return MODEL.classes_[i], float(proba[i])
