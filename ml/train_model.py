import os
import sys
import json
import pickle
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

# Ensure backend directory is in path to import simulator
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.simulator import GradeChangeSimulator

def engineer_features(df: pd.DataFrame, horizon: int = 120) -> tuple:
    """Engineer features and create future breach targets."""
    # Ensure sorted by run_id and timestamp
    df = df.sort_values(["run_id", "timestamp"]).reset_index(drop=True)
    
    # List of sensors to engineer rolling features for
    sensors = ["stock_flow", "machine_speed", "steam_pressure", "filler_flow", "moisture", "ash", "basis_weight"]
    
    features_df = df.copy()
    
    # 1. Rolling statistics (window of 15 seconds)
    for s in sensors:
        features_df[f"{s}_roll_mean_15"] = df.groupby("run_id")[s].transform(lambda x: x.rolling(15, min_periods=1).mean())
        features_df[f"{s}_roll_std_15"] = df.groupby("run_id")[s].transform(lambda x: x.rolling(15, min_periods=1).std().fillna(0))
        # Rate of change (slope over 15 seconds)
        features_df[f"{s}_rate_15"] = df.groupby("run_id")[s].transform(lambda x: (x - x.shift(15)).fillna(0) / 15.0)
    
    # 2. Recipe difference features
    features_df["bw_error"] = df["basis_weight"] - df["basis_weight_sp"]
    features_df["moisture_error"] = df["moisture"] - df["moisture_sp"]
    features_df["ash_error"] = df["ash"] - df["ash_sp"]
    features_df["speed_error"] = df["machine_speed"] - df["machine_speed_sp"]
    features_df["steam_error"] = df["steam_pressure"] - df["steam_pressure_sp"]
    features_df["stock_error"] = df["stock_flow"] - df["stock_flow_sp"]
    
    # 3. Future breach target label (Horizon: next 'horizon' seconds)
    # Target = 1 if the deviation > 2.5% at any point in the next 'horizon' steps
    features_df["deviation_pct"] = (features_df["basis_weight"] - features_df["basis_weight_sp"]).abs() / features_df["basis_weight_sp"]
    features_df["is_breached"] = (features_df["deviation_pct"] > 0.025).astype(int)
    
    # Lookahead target label
    # Group by run_id, shift backwards to check future values
    # We use a rolling max on the reversed series
    features_df["target_breach"] = (
        features_df.iloc[::-1]
        .groupby("run_id")["is_breached"]
        .rolling(horizon, min_periods=1)
        .max()
        .iloc[::-1]
        .reset_index(level=0, drop=True)
        .astype(int)
    )
    
    # Remove rows that are already in breach to focus on predicting FUTURE breaches (lead time)
    # Or keep them but separate them. Let's keep them and let the model learn the transitions.
    # To avoid predicting "breach" when it is already breached, we can create a flag "already_breached"
    features_df["already_breached"] = features_df["is_breached"]
    
    # Feature column names
    feature_cols = [
        "stock_flow", "machine_speed", "steam_pressure", "filler_flow", "moisture", "ash", "basis_weight",
        "basis_weight_sp", "moisture_sp", "ash_sp", "machine_speed_sp", "stock_flow_sp", "filler_flow_sp", "steam_pressure_sp",
        "bw_error", "moisture_error", "ash_error", "speed_error", "steam_error", "stock_error",
        "already_breached"
    ]
    for s in sensors:
        feature_cols.extend([f"{s}_roll_mean_15", f"{s}_roll_std_15", f"{s}_rate_15"])
        
    return features_df, feature_cols

def train_model():
    print("Generating simulation runs...")
    sim = GradeChangeSimulator()
    df = sim.generate_training_runs(count=40)
    
    print(f"Generated dataset with {len(df)} rows. Engineering features...")
    features_df, feature_cols = engineer_features(df)
    
    X = features_df[feature_cols]
    y = features_df["target_breach"]
    
    print(f"Features count: {len(feature_cols)}. Class distribution: {y.value_counts().to_dict()}")
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("Training XGBoost Classifier...")
    model = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        eval_metric="logloss"
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]
    
    print("Classification Report:")
    print(classification_report(y_test, preds))
    print(f"ROC AUC Score: {roc_auc_score(y_test, probs):.4f}")
    
    # Save model and feature names
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    model_path = os.path.join(os.path.dirname(__file__), "xgboost_model.json")
    model.save_model(model_path)
    
    meta_path = os.path.join(os.path.dirname(__file__), "model_metadata.pkl")
    with open(meta_path, "wb") as f:
        pickle.dump({
            "feature_cols": feature_cols,
            "sensors": ["stock_flow", "machine_speed", "steam_pressure", "filler_flow", "moisture", "ash", "basis_weight"]
        }, f)
    
    print(f"Model and metadata saved successfully to {os.path.dirname(__file__)}")

if __name__ == "__main__":
    train_model()
