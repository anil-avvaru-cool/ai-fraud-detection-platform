"""Investigator feedback loop — confirms/clears/escalates → label store.

Captures investigator outcomes to close the training data loop.
Confirmed labels feed the retraining pipeline.
Planned Week 5.
"""
from __future__ import annotations


class InvestigatorFeedbackLoop:
    """Captures investigator decisions and writes to label store."""

    def confirm_fraud(self, claim_id: str, investigator_id: str, notes: str) -> dict:
        raise NotImplementedError("Week 5")

    def clear_claim(self, claim_id: str, investigator_id: str, notes: str) -> dict:
        raise NotImplementedError("Week 5")

    def escalate(self, claim_id: str, investigator_id: str, escalation_reason: str) -> dict:
        raise NotImplementedError("Week 5")
