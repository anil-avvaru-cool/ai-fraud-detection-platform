"""Decision orchestration — tier routing + adverse action documentation.

Routes fraud scores to appropriate action based on tier thresholds from config.py.
Planned Week 4.
"""
from __future__ import annotations

from config import TIER_EVIDENCE_MAX, TIER_HOLD_MIN, TIER_SIU_MAX, TIER_STP_MAX


def get_decision_tier(fraud_score: float) -> str:
    """Map fraud score to decision tier name."""
    if fraud_score < TIER_STP_MAX:
        return "stp"
    if fraud_score < TIER_EVIDENCE_MAX:
        return "evidence_request"
    if fraud_score < TIER_SIU_MAX:
        return "siu_referral"
    return "payment_hold"


class DecisionOrchestrator:
    """Routes fraud scores to actions; generates adverse action documentation."""

    def orchestrate(self, claim_id: str, fraud_score: float, shap_factors: list[dict]) -> dict:
        """Return decision tier and required actions."""
        raise NotImplementedError("Week 4")
