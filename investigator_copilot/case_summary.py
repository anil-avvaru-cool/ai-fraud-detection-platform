"""Investigator Copilot — auto-generated case brief + evidence checklist.

Generates SHAP-based case summaries and dynamic evidence checklists for
human investigators. HITL workflow for SIU referral and payment holds.
Planned Week 5.
"""
from __future__ import annotations


class CaseSummaryGenerator:
    """Generates structured case summaries for fraud investigators."""

    def generate_case_brief(self, claim_id: str, fraud_score: float, shap_factors: list[dict]) -> dict:
        """Generate case brief with fraud risk summary, evidence checklist, and graph context."""
        raise NotImplementedError("Week 5")

    def generate_evidence_checklist(self, fraud_score: float, shap_factors: list[dict]) -> list[str]:
        """Dynamic checklist based on top SHAP factors."""
        raise NotImplementedError("Week 5")
