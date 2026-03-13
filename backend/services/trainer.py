import json
import os
from typing import List, Dict, Tuple
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import f1_score, accuracy_score
from scipy.sparse import hstack, csr_matrix
import joblib

# Support both package and module execution
from core.config import settings

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
    df = pd.DataFrame(rows)
    metadata_file = os.path.join(settings.data_dir, "metadata.jsonl")
    if os.path.exists(metadata_file):
        try:
            meta_rows = []
            with open(metadata_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        meta_rows.append(json.loads(line))
                    except Exception:
                        continue
            if meta_rows and len(meta_rows) == len(df):
                meta_df = pd.DataFrame(meta_rows)
                df["features"] = meta_df["features"]
                df["document_type"] = meta_df["document_type"]
                df["language"] = meta_df["language"]
                df["has_metadata"] = True
            else:
                df["has_metadata"] = False
        except Exception as e:
            print(f"Warning: Could not load metadata, using text-only training: {e}")
            df["has_metadata"] = False
    else:
        df["has_metadata"] = False
    return df

def train_model() -> Tuple[float, float]:
    df = _load_training_df()
    if df.empty:
        raise RuntimeError("No training data available.")
    X_text = df["text"].tolist()
    y_labels = df["labels"].tolist()
    use_metadata = df.get("has_metadata", pd.Series([False])).iloc[0] if len(df) > 0 else False
    mlb = MultiLabelBinarizer(classes=CATEGORIES)
    Y = mlb.fit_transform(y_labels)
    X_train_text, X_test_text, Y_train, Y_test = train_test_split(
        X_text, Y, test_size=0.2, random_state=42
    )
    vectorizer = TfidfVectorizer(max_features=20000, ngram_range=(1, 2))
    X_train_tfidf = vectorizer.fit_transform(X_train_text)
    X_test_tfidf = vectorizer.transform(X_test_text)
    if use_metadata:
        print("Training with enhanced metadata features...")
        train_indices = df.index[:len(X_train_text)]
        test_indices = df.index[len(X_train_text):]
        train_meta_features = _extract_feature_vectors(df.iloc[train_indices])
        test_meta_features = _extract_feature_vectors(df.iloc[test_indices])
        X_train_combined = hstack([X_train_tfidf, csr_matrix(train_meta_features)])
        X_test_combined = hstack([X_test_tfidf, csr_matrix(test_meta_features)])
        X_train_final = X_train_combined
        X_test_final = X_test_combined
    else:
        print("Training with text features only...")
        X_train_final = X_train_tfidf
        X_test_final = X_test_tfidf
    base_clf = LogisticRegression(max_iter=200)
    clf = OneVsRestClassifier(base_clf)
    clf.fit(X_train_final, Y_train)
    Y_pred = clf.predict(X_test_final)
    acc = accuracy_score(Y_test, Y_pred)
    f1 = f1_score(Y_test, Y_pred, average="micro")
    model_bundle = {
        "vectorizer": vectorizer,
        "classifier": clf,
        "mlb": mlb,
        "use_metadata": use_metadata,
    }
    joblib.dump(model_bundle, settings.model_file)
    with open(settings.metrics_file, "w", encoding="utf-8") as f:
        json.dump({
            "accuracy": acc,
            "f1_micro": f1,
            "use_metadata": use_metadata,
        }, f, indent=2)
    return acc, f1

def _extract_feature_vectors(df_subset: pd.DataFrame) -> np.ndarray:
    feature_vectors = []
    for idx, row in df_subset.iterrows():
        features = row.get("features", {})
        feature_vec = [
            int(features.get("has_currency", False)),
            int(features.get("has_percentage", False)),
            int(features.get("has_date", False)),
            int(features.get("has_duration", False)),
            features.get("legal_keyword_count", 0),
            features.get("risk_keyword_count", 0),
            int(features.get("has_numbered_clauses", False)),
            int(features.get("has_party_identification", False)),
            int(features.get("has_payment_terms", False)),
            int(features.get("has_installment", False)),
            int(features.get("has_deadline", False)),
            int(features.get("has_timeframe", False)),
        ]
        doc_type = row.get("document_type", "general")
        doc_type_vec = [
            int(doc_type == "construction_contract"),
            int(doc_type == "employment_contract"),
            int(doc_type == "loan_agreement"),
            int(doc_type == "sales_contract"),
        ]
        feature_vec.extend(doc_type_vec)
        language = row.get("language", "unknown")
        lang_vec = [
            int(language == "khmer"),
            int(language == "english"),
            int(language == "mixed"),
        ]
        feature_vec.extend(lang_vec)
        feature_vectors.append(feature_vec)
    return np.array(feature_vectors)

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
