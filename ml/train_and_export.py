import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

DATA_PATH = "data/online_shoppers_intention.csv"
ARTIFACT_DIR = "artifacts"
MODEL_PATH = os.path.join(ARTIFACT_DIR, "model.joblib")

def main():
    print("Loading data...")  # ← ADD THIS
    df = pd.read_csv(DATA_PATH)
    print(f"Data shape: {df.shape}")  # ← ADD THIS

    # target
    df["Revenue"] = df["Revenue"].map({True: 1, False: 0}).astype(int)

    X = df.drop(columns=["Revenue"])
    y = df["Revenue"]

    # treat ID-like integer columns as categorical
    id_like = ["OperatingSystems", "Browser", "Region", "TrafficType"]
    for c in id_like:
        X[c] = X[c].astype(str)

    num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_cols = [c for c in X.columns if c not in num_cols]
    
    print(f"Numeric features: {len(num_cols)}")  # ← ADD THIS
    print(f"Categorical features: {len(cat_cols)}")  # ← ADD THIS

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    numeric_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_pipe, num_cols),
        ("cat", categorical_pipe, cat_cols),
    ])

    model = Pipeline([
        ("prep", preprocessor),
        ("clf", LogisticRegression(max_iter=3000, class_weight="balanced")),
    ])

    print("Training model...")  # ← ADD THIS
    model.fit(X_train, y_train)
    
    probs = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, probs)

    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    joblib.dump(
        {
            "model": model,
            "num_cols": num_cols,
            "cat_cols": cat_cols,
            "base_rate": float(y.mean()),
        },
        MODEL_PATH
    )

    print("\n✅ Training Complete!")  # ← ADD THIS
    print("Saved:", MODEL_PATH)
    print("Baseline ROC-AUC:", round(auc, 4))
    print("Base conversion rate:", round(float(y.mean()), 4))

if __name__ == "__main__":
    main()
