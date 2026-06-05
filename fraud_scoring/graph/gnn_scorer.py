"""GNN fraud scorer — GraphSAGE on the Neo4j claim graph.

Planned Week 6. Uses graph neighborhood features to score
claim fraud probability from network context.
"""
from __future__ import annotations


class GNNFraudScorer:
    """GraphSAGE-based fraud scorer (async path only)."""

    def score(self, claim_id: str) -> float | None:
        """Return P(fraud | graph neighborhood). None while not yet trained."""
        return None  # stub — GraphSAGE training planned Week 6
