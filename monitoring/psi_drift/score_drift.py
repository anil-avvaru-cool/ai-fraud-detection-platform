"""Fraud score PSI drift monitoring — keyed on fnol_submitted_at.

Tracks distribution shifts in fraud scores and claim features.
Imports shared PSI implementation from insurance-data-platform.
Planned Week 7.
"""
from __future__ import annotations

from pathlib import Path

from config import CLAIMS_OUTPUT, PSI_CURRENT_WINDOW_DAYS, PSI_MIN_RECORDS, PSI_REFERENCE_VERSION


def run_score_drift_check(
    claims_path: Path = CLAIMS_OUTPUT,
    as_of=None,
) -> dict:
    """Run PSI drift check on fraud score features, keyed on fnol_submitted_at."""
    raise NotImplementedError("Week 7 — PSI drift monitoring")
