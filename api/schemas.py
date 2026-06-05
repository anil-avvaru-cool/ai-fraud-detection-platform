"""Pydantic schemas for the fraud detection API.

DEC-009: schemas defined here as Pydantic models, not standalone JSON Schema files.
JSON Schema can be generated on demand via model.model_json_schema() when needed.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class ClaimSyncRequest(BaseModel):
    """Input schema for synchronous fraud scoring (/score/sync)."""

    claim_id: str
    quote_id: str
    state: str
    policy_inception_days: int = 0
    prior_claims_count: int = 0
    reported_injury_count: int = 0
    reporting_delay_days: int = 0
    attorney_present: bool = False
    claimant_count: int = 1
    submission_hour: int = 12
    graph_hop_distance: int | None = None
    shared_attribute_count: int = 0
    attorney_centrality_score: float = 0.0
    narrative_inconsistency_score: float = 0.0
    narrative_complexity_score: float = 0.0
    risk_score_at_issuance: float | None = None
    ip_geolocation_delta_miles: float = 0.0
    device_fingerprint_match: bool = True
    telematics_distraction_score: float | None = None
    telematics_hard_brake_rate: float | None = None
    telematics_crash_match: float | None = None
    telematics_commute_entropy: float | None = None
    telematics_enrolled: bool = False


class FraudScoreResponse(BaseModel):
    """Output schema for fraud scoring endpoints."""

    claim_id: str
    fraud_score: float = Field(ge=0.0, le=1.0)
    ci_lower: float
    ci_upper: float
    decision_tier: str
    p_xgb: float
    p_anomaly: float
    p_gnn: float | None = None
    p_nlp: float | None = None
    p_vision: float | None = None
    top_shap_factors: list[dict]
    latency_ms: float | None = None


class ExplanationResponse(BaseModel):
    """SHAP explanation response."""

    claim_id: str
    fraud_score: float
    top_factors: list[dict]
    adverse_action_notice: str | None = None
