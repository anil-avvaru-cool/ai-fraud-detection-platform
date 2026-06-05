"""Stage 4c — Stacking meta-learner → fraud_score [0,1] + CI.

Architecture:
  XGBoost fraud     → P(fraud | structured features)           [trained]
  Isolation Forest  → anomaly score                            [trained, unsupervised]
  GNN               → P(fraud | network context)               [stub — GraphSAGE emerging]
  NLP Transformer   → P(fraud | narrative inconsistency)       [proxy from feature]
  Vision ViT/CLIP   → P(fraud | image tampering)               [stub — emerging]
          │
          ▼
  Stacking Meta-Learner  (LogisticRegression, trained on 5-fold OOF)
          │
          ▼
   Final Fraud Score [0.0 – 1.0]  +  Confidence Interval
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
import shap
import xgboost as xgb
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

from fraud_scoring.anomaly.anomaly_detector import (
    _compute_medians,
    _impute,
    decision_to_anomaly_score,
    train_anomaly_detector,
)
from fraud_scoring.ensemble.tabular_model import (
    CLAIM_FRAUD_FEATURE_COLS,
    TARGET,
    _ensure_risk_score,
    prepare_fraud_features,
    train as train_xgb_fraud,
)

# Explicit signal registry — meta-learner sees only trained channels.
ACTIVE_SIGNALS: list[str] = ["p_xgb", "p_anomaly"]
PENDING_SIGNALS: list[str] = ["p_gnn", "p_nlp", "p_vision"]


def train_stacking(claims_path: Path, quotes_path: Path, output_dir: Path) -> dict:
    """Train the stacking meta-learner via 5-fold OOF; saves fraud_meta_learner.json."""
    df = pd.read_parquet(claims_path)
    df = _ensure_risk_score(df, quotes_path)
    df = prepare_fraud_features(df).dropna(subset=[TARGET]).reset_index(drop=True)

    available_cols = [c for c in CLAIM_FRAUD_FEATURE_COLS if c in df.columns]
    X_df = df[available_cols]
    y = df[TARGET].astype(int).values

    xgb_oof = np.zeros(len(df))
    anomaly_oof = np.zeros(len(df))

    kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    for train_idx, val_idx in kfold.split(X_df, y):
        X_tr = X_df.iloc[train_idx]
        X_val = X_df.iloc[val_idx]
        y_tr = y[train_idx]

        neg, pos = int((y_tr == 0).sum()), int((y_tr == 1).sum())
        spw = neg / max(pos, 1)

        m_xgb = xgb.XGBClassifier(
            objective="binary:logistic",
            n_estimators=300,
            max_depth=5,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            scale_pos_weight=spw,
            tree_method="hist",
            random_state=42,
            verbosity=0,
        )
        m_xgb.fit(X_tr, y_tr, verbose=False)
        xgb_oof[val_idx] = m_xgb.predict_proba(X_val)[:, 1]

        fold_medians = _compute_medians(X_tr, available_cols)
        X_tr_imp = _impute(X_tr, fold_medians).values
        X_val_imp = _impute(X_val, fold_medians).values

        contamination = float(np.clip(y_tr.mean(), 0.05, 0.5))
        m_iso = IsolationForest(n_estimators=100, contamination=contamination, random_state=42, n_jobs=-1)
        m_iso.fit(X_tr_imp)
        anomaly_oof[val_idx] = decision_to_anomaly_score(m_iso.decision_function(X_val_imp))

    oof = {"p_xgb": xgb_oof, "p_anomaly": anomaly_oof}
    meta_X = np.column_stack([oof[s] for s in ACTIVE_SIGNALS])
    meta_lr = LogisticRegression(C=1.0, solver="lbfgs", max_iter=500, random_state=42)
    meta_lr.fit(meta_X, y)

    fraud_score_oof = meta_lr.predict_proba(meta_X)[:, 1]
    auc = float(roc_auc_score(y, fraud_score_oof))
    gini = 2 * auc - 1

    meta_artifact = {
        "method": "logistic_regression",
        "coef": meta_lr.coef_[0].tolist(),
        "intercept": float(meta_lr.intercept_[0]),
        "input_features": ACTIVE_SIGNALS,
        "cv_folds": 5,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "fraud_meta_learner.json").write_text(json.dumps(meta_artifact, indent=2))

    metrics = {
        "oof_auc": round(auc, 4),
        "oof_gini": round(gini, 4),
        "n_records": len(df),
        "coef_p_xgb": round(float(meta_lr.coef_[0][0]), 4),
        "coef_p_anomaly": round(float(meta_lr.coef_[0][1]), 4),
        "intercept": round(float(meta_lr.intercept_[0]), 4),
    }
    (output_dir / "fraud_meta_metrics.json").write_text(json.dumps(metrics, indent=2))
    return metrics


class EnsembleFraudScorer:
    """Load trained fraud ensemble components and score claims."""

    def __init__(self, model_dir: Path) -> None:
        self._xgb = xgb.XGBClassifier()
        self._xgb.load_model(model_dir / "fraud_model.json")

        self._iso: IsolationForest = joblib.load(model_dir / "fraud_anomaly_model.joblib")
        self._anomaly_medians: dict[str, float] = json.loads(
            (model_dir / "fraud_anomaly_medians.json").read_text()
        )

        meta = json.loads((model_dir / "fraud_meta_learner.json").read_text())
        self._meta_coef = np.array(meta["coef"])
        self._meta_intercept = float(meta["intercept"])

        features_path = model_dir / "fraud_features.json"
        self._feature_cols: list[str] = (
            json.loads(features_path.read_text())
            if features_path.exists()
            else list(CLAIM_FRAUD_FEATURE_COLS)
        )

        self._xgb_explainer: shap.TreeExplainer | None = None

    def _xgb_score(self, X: pd.DataFrame) -> np.ndarray:
        return self._xgb.predict_proba(X)[:, 1]

    def _anomaly_score(self, X: pd.DataFrame) -> np.ndarray:
        X_imp = _impute(X, self._anomaly_medians).values
        return decision_to_anomaly_score(self._iso.decision_function(X_imp))

    def _meta_sigmoid(self, signal_values: dict[str, np.ndarray]) -> np.ndarray:
        stacked = np.column_stack([signal_values[s] for s in ACTIVE_SIGNALS])
        logit = stacked @ self._meta_coef + self._meta_intercept
        return 1.0 / (1.0 + np.exp(-logit))

    def score(self, df: pd.DataFrame) -> pd.DataFrame:
        """Score claims. Returns DataFrame with fraud_score + CI + per-signal scores."""
        df_prep = prepare_fraud_features(df)
        X = df_prep[self._feature_cols]

        p_xgb = self._xgb_score(X)
        p_anomaly = self._anomaly_score(X)

        # Pending channels — untrained; None prevents accidental meta-learner inclusion
        p_gnn = None    # GraphSAGE — Week 6
        p_nlp = None    # NLP transformer — Week 6
        p_vision = None  # ViT image tampering — Week 6

        active_scores = {"p_xgb": p_xgb, "p_anomaly": p_anomaly}
        fraud_score = self._meta_sigmoid(active_scores)

        base_scores = np.column_stack([active_scores[s] for s in ACTIVE_SIGNALS])
        score_std = base_scores.std(axis=1)
        ci_lower = np.clip(fraud_score - 1.96 * score_std, 0.0, 1.0)
        ci_upper = np.clip(fraud_score + 1.96 * score_std, 0.0, 1.0)

        return pd.DataFrame(
            {
                "fraud_score": fraud_score,
                "ci_lower": ci_lower,
                "ci_upper": ci_upper,
                "p_xgb": p_xgb,
                "p_anomaly": p_anomaly,
                "p_gnn": p_gnn,
                "p_nlp": p_nlp,
                "p_vision": p_vision,
            },
            index=df.index,
        )

    def explain(self, df: pd.DataFrame, top_n: int = 5) -> list[list[dict[str, Any]]]:
        """Per-row SHAP reason codes from the XGBoost fraud model."""
        if self._xgb_explainer is None:
            self._xgb_explainer = shap.TreeExplainer(self._xgb)

        X = prepare_fraud_features(df)[self._feature_cols]
        shap_values = self._xgb_explainer.shap_values(X)

        results: list[list[dict[str, Any]]] = []
        for row_shap in shap_values:
            abs_total = float(np.abs(row_shap).sum()) or 1.0
            ranked = sorted(enumerate(row_shap), key=lambda x: abs(x[1]), reverse=True)[:top_n]
            results.append([
                {"feature": self._feature_cols[i], "shap_pct": round(float(v) / abs_total * 100, 1)}
                for i, v in ranked
            ])
        return results


def train_ensemble(claims_path: Path, quotes_path: Path, output_dir: Path) -> dict:
    """Orchestrate all three fraud ensemble training stages."""
    xgb_metrics = train_xgb_fraud(claims_path, quotes_path, output_dir)
    anomaly_metrics = train_anomaly_detector(claims_path, quotes_path, output_dir)
    stacking_metrics = train_stacking(claims_path, quotes_path, output_dir)
    return {
        "xgb_fraud": xgb_metrics,
        "anomaly_detector": anomaly_metrics,
        "stacking_meta_learner": stacking_metrics,
    }
