"""SHAP explainability — top-5 SHAP + counterfactuals + adverse action generation.

Wraps EnsembleFraudScorer.explain() with adverse action documentation
for regulatory compliance. Planned Week 4.
"""
from __future__ import annotations

from pathlib import Path


class FraudSHAPExplainer:
    """Generates SHAP-based explanations for fraud scoring decisions."""

    def explain(self, claim_df, top_n: int = 5) -> list[dict]:
        raise NotImplementedError("Week 4")

    def generate_adverse_action_notice(self, shap_factors: list[dict], state: str) -> str:
        raise NotImplementedError("Week 4")
