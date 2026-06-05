"""SHAP snapshot monitoring for the fraud XGBoost model.

Tracks global mean |SHAP| values across retraining cycles.
Planned Week 7.
"""
from __future__ import annotations

from pathlib import Path

from config import FRAUD_MODELS_DIR


def write_shap_snapshot(model_dir: Path = FRAUD_MODELS_DIR, output_dir: Path = FRAUD_MODELS_DIR) -> Path:
    """Compute and write global SHAP snapshot for the fraud XGBoost model."""
    raise NotImplementedError("Week 7")


def compare_shap_snapshots(output_dir: Path = FRAUD_MODELS_DIR) -> dict:
    """Compare two most recent SHAP snapshots for brittleness detection."""
    raise NotImplementedError("Week 7")
