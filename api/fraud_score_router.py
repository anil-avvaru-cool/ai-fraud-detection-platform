"""FastAPI router — /score/sync, /score/async, /explanation.

Planned Week 4.
"""
from __future__ import annotations

from fastapi import APIRouter

from api.schemas import ClaimSyncRequest, ExplanationResponse, FraudScoreResponse

router = APIRouter(prefix="/score", tags=["fraud-scoring"])


@router.post("/sync", response_model=FraudScoreResponse)
async def score_sync(request: ClaimSyncRequest) -> FraudScoreResponse:
    """Synchronous fraud scoring — <100ms, blocks FNOL submission."""
    raise NotImplementedError("Week 4 — sync inference path")


@router.post("/async")
async def score_async(request: ClaimSyncRequest) -> dict:
    """Asynchronous fraud scoring — triggers deep enrichment pipeline."""
    raise NotImplementedError("Week 5 — async enrichment path")


@router.get("/explanation/{claim_id}", response_model=ExplanationResponse)
async def get_explanation(claim_id: str) -> ExplanationResponse:
    """Retrieve SHAP-based explanation for a scored claim."""
    raise NotImplementedError("Week 4 — SHAP explanation endpoint")
