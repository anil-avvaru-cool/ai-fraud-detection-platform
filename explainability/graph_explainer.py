"""Graph explainer — fraud ring path → human-readable case narrative.

Converts Neo4j fraud ring paths into natural-language explanations
for the investigator copilot. Planned Week 5.
"""
from __future__ import annotations


class GraphPathExplainer:
    """Converts fraud ring graph paths to human-readable explanations."""

    def explain_path(self, claim_id: str, ring_path: list[dict]) -> str:
        raise NotImplementedError("Week 5")
