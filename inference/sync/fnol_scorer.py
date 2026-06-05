"""Synchronous FNOL fraud scoring — <100ms path, blocks FNOL submission.

Latency budget (from config.py):
  ~5ms   Online feature retrieval (Redis)
  ~10ms  Device reputation lookup
  ~20ms  Graph neighborhood query (1–2 hops)
  ~5ms   Tabular XGBoost scoring
  ~15ms  Lightweight image hash check
  ~10ms  Decision orchestration + routing
  ────────────────────────────────
  ~65ms  Total (target < 100ms)

Planned Week 4.
"""
from __future__ import annotations

from pathlib import Path


class FNOLSyncScorer:
    """<100ms synchronous fraud scoring path for FNOL intake."""

    def __init__(self, model_dir: Path) -> None:
        self._model_dir = model_dir

    def score(self, claim_payload: dict) -> dict:
        """Score a claim synchronously. Returns fraud_score + decision tier."""
        raise NotImplementedError("Week 4 — sync inference path")
