import json
import os
from typing import List, Dict, Tuple

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import f1_score, accuracy_score
import joblib

# Support both package and module execution
try:
    from .config import settings
except ImportError:
    from config import settings


CATEGORIES = [
    "Financial",
    "Schedule",
    "Technical",
    "Legal",
    "Operational",
    "Compliance",
    "Other",
]


def append_training_example(text: str, risks: List[Dict]):
    """Store training data as JSONL with text and labels from LLM output."""
    labels = sorted({r.get("category", "Other") for r in risks})
    rec = {"text": text, "labels": labels, "raw": risks}
    with open(settings.training_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _load_training_df() -> pd.DataFrame:
    rows = []
    if not os.path.exists(settings.training_file):
        return pd.DataFrame(columns=["text", "labels"])
    with open(settings.training_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
                rows.append({"text": obj.get("text", ""), "labels": obj.get("labels", [])})
            except Exception:
                continue
    return pd.DataFrame(rows)


def train_model() -> Tuple[float, float]:
    """Train a simple multi-label classifier and persist the model and metrics.
    Returns (accuracy, f1_micro).
    """
    df = _load_training_df()
    if df.empty:
        raise RuntimeError("No training data available.")

    X = df["text"].tolist()
    y_labels = df["labels"].tolist()

    mlb = MultiLabelBinarizer(classes=CATEGORIES)
    Y = mlb.fit_transform(y_labels)

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    vectorizer = TfidfVectorizer(max_features=20000, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    base_clf = LogisticRegression(max_iter=200)
    clf = OneVsRestClassifier(base_clf)
    clf.fit(X_train_vec, Y_train)

    Y_pred = clf.predict(X_test_vec)
    acc = accuracy_score(Y_test, Y_pred)
    f1 = f1_score(Y_test, Y_pred, average="micro")

    joblib.dump({"vectorizer": vectorizer, "classifier": clf, "mlb": mlb}, settings.model_file)
    with open(settings.metrics_file, "w", encoding="utf-8") as f:
        json.dump({"accuracy": acc, "f1_micro": f1}, f, indent=2)

    return acc, f1


def model_ready() -> bool:
    return os.path.exists(settings.model_file)


def predict_categories(text: str) -> List[str]:
    if not model_ready():
        return []
    bundle = joblib.load(settings.model_file)
    vectorizer = bundle["vectorizer"]
    clf = bundle["classifier"]
    mlb = bundle["mlb"]
    X_vec = vectorizer.transform([text])
    Y_pred = clf.predict(X_vec)
    labels = mlb.inverse_transform(Y_pred)
    return sorted(labels[0]) if labels else []