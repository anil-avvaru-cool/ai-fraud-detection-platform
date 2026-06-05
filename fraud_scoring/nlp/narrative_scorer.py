"""NLP Transformer narrative scorer.

Scores narrative inconsistency + complexity from claim text.
Planned Week 6. Currently proxied from pre-computed features in the claims parquet.
"""
from __future__ import annotations


class NarrativeScorer:
    """NLP-based narrative inconsistency and complexity scoring."""

    def score(self, narrative_text: str) -> dict | None:
        """Return narrative_inconsistency_score, narrative_complexity_score.
        Returns None while transformer model is not trained.
        """
        return None  # stub — NLP transformer planned Week 6
