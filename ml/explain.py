import os
import sys
import pickle
import numpy as np
import pandas as pd
import shap
from xgboost import XGBClassifier
from typing import Dict, Any, List

class GradeSenseExplainer:
    def __init__(self):
        self.model_dir = os.path.dirname(__file__)
        self.model_path = os.path.join(self.model_dir, "xgboost_model.json")
        self.meta_path = os.path.join(self.model_dir, "model_metadata.pkl")
        
        self.model = None
        self.feature_cols = []
        self.explainer = None
        
    def load(self):
        if not os.path.exists(self.model_path) or not os.path.exists(self.meta_path):
            raise FileNotFoundError("Model or metadata file not found. Run train_model.py first.")
            
        with open(self.meta_path, "rb") as f:
            meta = pickle.load(f)
            self.feature_cols = meta["feature_cols"]
            
        self.model = XGBClassifier()
        self.model.load_model(self.model_path)
        
        # Initialize TreeExplainer
        self.explainer = shap.TreeExplainer(self.model)

    def explain(self, features_df: pd.DataFrame) -> Dict[str, Any]:
        """Explain a single input data row (usually the last row of streaming window)."""
        if self.model is None:
            self.load()
            
        # Ensure we only use the specified feature columns
        X = features_df[self.feature_cols].copy()
        
        # Compute probabilities
        prob = float(self.model.predict_proba(X)[:, 1][-1])
        
        # Compute SHAP values
        shap_values = self.explainer.shap_values(X)
        
        # Get SHAP values for the last row
        last_row_shap = shap_values[-1]
        
        # Map feature names to SHAP values
        contributions = []
        for col, val in zip(self.feature_cols, last_row_shap):
            contributions.append({
                "feature": col,
                "val": float(val)
            })
            
        # Sort by absolute SHAP value
        contributions = sorted(contributions, key=lambda x: abs(x["val"]), reverse=True)
        
        # Format contributing factors for the UI
        ui_contributions = []
        total_abs = sum(abs(c["val"]) for c in contributions)
        
        for c in contributions[:5]: # top 5
            pct = (abs(c["val"]) / total_abs * 100) if total_abs > 0 else 0
            direction = "increase" if c["val"] > 0 else "decrease"
            ui_contributions.append({
                "feature": c["feature"],
                "impact": float(c["val"]),
                "percentage": round(pct, 1),
                "direction": direction
            })
            
        # Generate plain text sentence
        explanation_sentence = self._generate_sentence(ui_contributions, X.iloc[-1])
        
        return {
            "risk_score": round(prob * 100, 1),
            "contributions": ui_contributions,
            "explanation": explanation_sentence,
            "source_of_inference": "XGBoost + SHAP Explainability Engine"
        }
        
    def _generate_sentence(self, top_factors: List[Dict[str, Any]], last_row: pd.Series) -> str:
        """Create a clean human-readable explanation from the top SHAP features."""
        # Map technical feature names to friendly descriptions
        friendly_names = {
            "stock_flow": "stock flow rate",
            "machine_speed": "machine speed",
            "steam_pressure": "steam drying pressure",
            "filler_flow": "filler clay flow",
            "moisture": "paper moisture level",
            "ash": "sheet ash content",
            "basis_weight": "basis weight",
            "bw_error": "basis weight target deviation",
            "moisture_error": "moisture control error",
            "steam_error": "dryer steam error",
            "speed_error": "machine speed error",
            "stock_error": "stock flow deviation",
            "already_breached": "existing limit breach"
        }
        
        reasons = []
        for f in top_factors[:3]:
            feat_name = f["feature"]
            # Look up clean name
            clean_name = friendly_names.get(feat_name, feat_name)
            if "_roll_" in feat_name:
                base = feat_name.split("_roll_")[0]
                clean_name = f"rolling average of {friendly_names.get(base, base)}"
            elif "_rate_" in feat_name:
                base = feat_name.split("_rate_")[0]
                clean_name = f"rate of change in {friendly_names.get(base, base)}"
                
            # Describe direction of change or state
            val = last_row[feat_name]
            direction = f["direction"]
            
            if "error" in feat_name or "deviation" in feat_name:
                if val > 0:
                    reasons.append(f"{clean_name} is higher than recipe target")
                else:
                    reasons.append(f"{clean_name} lags below recipe target")
            else:
                if direction == "increase":
                    reasons.append(f"high/increasing {clean_name}")
                else:
                    reasons.append(f"low/decreasing {clean_name}")
                    
        if not reasons:
            return "Process conditions are currently stable within baseline limits."
            
        sentence = "Risk is driven by: " + ", ".join(reasons[:-1])
        if len(reasons) > 1:
            sentence += f" and {reasons[-1]}."
        else:
            sentence += "."
            
        return sentence
