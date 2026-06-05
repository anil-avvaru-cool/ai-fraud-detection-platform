"""Champion-Challenger framework for the fraud detection platform.

Four-stage loop: Shadow → Gini check → Phased rollout → Promote.
Mirrors the underwriting platform's CC framework but operates on fraud models.
Planned Week 6.
"""
from __future__ import annotations

from pathlib import Path

from config import CLAIMS_OUTPUT, FRAUD_MODELS_DIR


def score_shadow(claims_path: Path = CLAIMS_OUTPUT, models_dir: Path = FRAUD_MODELS_DIR) -> Path:
    """Run challenger fraud model in shadow mode."""
    raise NotImplementedError("Week 6")


def compare_gini(models_dir: Path = FRAUD_MODELS_DIR) -> dict:
    """Compare champion vs challenger fraud model Gini on shadow cohort."""
    raise NotImplementedError("Week 6")


def promote_challenger(models_dir: Path = FRAUD_MODELS_DIR) -> dict:
    """Promote challenger fraud model to champion slot."""
    raise NotImplementedError("Week 6")
