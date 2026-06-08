from __future__ import annotations

from fastapi import FastAPI

from api.fraud_score_router import router as fraud_router

app = FastAPI(title="AI Fraud Detection Platform", version="2026-Q2")

app.include_router(fraud_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
