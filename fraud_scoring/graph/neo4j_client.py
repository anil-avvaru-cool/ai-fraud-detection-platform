"""Neo4j client — sync (1–2 hop) + async (3+ hop) query helpers.

Sync path: neighborhood queries for the <100ms FNOL scoring window.
Async path: deep ring detection (3+ hop Louvain community traversal).
"""
from __future__ import annotations


class Neo4jFraudClient:
    """Wraps Neo4j driver for fraud graph queries."""

    def query_neighborhood_sync(self, claim_id: str, max_hops: int = 2) -> dict:
        """1–2 hop neighborhood for sync inference (<20ms budget)."""
        raise NotImplementedError("Week 4")

    def query_ring_async(self, claim_id: str, max_hops: int = 6) -> dict:
        """3+ hop ring detection for async enrichment path."""
        raise NotImplementedError("Week 5")
