"""Business rules engine — state DOI constraints, mandatory SIU triggers, exclusions.

Applies deterministic rules on top of model scores. Rules can override model
output (e.g., regulatory requirement to refer to SIU regardless of score).
Planned Week 4.
"""
from __future__ import annotations


class RulesEngine:
    """Applies state DOI constraints and business rules to fraud decisions."""

    def apply_rules(self, claim: dict, score: float, state: str) -> dict:
        """Apply rules; return updated action dict."""
        raise NotImplementedError("Week 4")
