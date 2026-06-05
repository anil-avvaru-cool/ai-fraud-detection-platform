"""Action router — dispatches to STP / evidence request / SIU / payment hold.

Planned Week 4.
"""
from __future__ import annotations


class ActionRouter:
    def route_stp(self, claim_id: str) -> dict:
        raise NotImplementedError("Week 4")

    def route_evidence_request(self, claim_id: str, required_docs: list[str]) -> dict:
        raise NotImplementedError("Week 4")

    def route_siu_referral(self, claim_id: str, reason_codes: list[str]) -> dict:
        raise NotImplementedError("Week 4")

    def route_payment_hold(self, claim_id: str, reason_codes: list[str]) -> dict:
        raise NotImplementedError("Week 4")
