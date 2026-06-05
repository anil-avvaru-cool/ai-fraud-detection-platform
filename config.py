"""AI Fraud Detection Platform configuration.

Tier thresholds, latency budgets, PSI config, Neo4j/Redis.
Data paths reference insurance-data-platform output directory.
"""
from __future__ import annotations

import os
from pathlib import Path

# ── Data paths ────────────────────────────────────────────────────────────────
_DEFAULT_DATA_ROOT = Path(__file__).resolve().parent.parent / "insurance-data-platform"
DATA_PLATFORM_ROOT = Path(os.environ.get("DATA_PLATFORM_ROOT", _DEFAULT_DATA_ROOT))

RAW_DATA_DIR = DATA_PLATFORM_ROOT / "data" / "raw"
CLAIMS_OUTPUT = RAW_DATA_DIR / "claims.parquet"
QUOTES_OUTPUT = RAW_DATA_DIR / "quotes.parquet"
PROCESSED_DATA_DIR = DATA_PLATFORM_ROOT / "data" / "processed"

# ── Model artifacts ───────────────────────────────────────────────────────────
_REPO_ROOT = Path(__file__).resolve().parent
FRAUD_MODELS_DIR = _REPO_ROOT / "models" / "artifacts"

# ── Decision tier thresholds (score ∈ [0, 1]) ─────────────────────────────────
TIER_STP_MAX: float = 0.25          # score < 0.25 → Straight-Through Processing
TIER_EVIDENCE_MAX: float = 0.60     # 0.25–0.60 → request additional evidence
TIER_SIU_MAX: float = 0.85          # 0.60–0.85 → SIU referral + payment delay
TIER_HOLD_MIN: float = 0.85         # > 0.85 → payment hold + mandatory investigation

# ── Synchronous path latency budgets (ms) ────────────────────────────────────
LATENCY_REDIS_MS: int = 5
LATENCY_DEVICE_MS: int = 10
LATENCY_GRAPH_MS: int = 20
LATENCY_XGB_MS: int = 5
LATENCY_IMAGE_HASH_MS: int = 15
LATENCY_ORCHESTRATION_MS: int = 10
LATENCY_SYNC_TOTAL_TARGET_MS: int = 100

# ── PSI drift monitoring ──────────────────────────────────────────────────────
PSI_REFERENCE_VERSION = "v1.0.0"
PSI_CURRENT_WINDOW_DAYS = 14
PSI_MIN_RECORDS = 500

# ── Neo4j ─────────────────────────────────────────────────────────────────────
NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "")

# ── Redis online feature store ────────────────────────────────────────────────
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
FEATURE_TTL_SECONDS: int = 3600

# ── API ───────────────────────────────────────────────────────────────────────
API_HOST = os.environ.get("API_HOST", "0.0.0.0")
API_PORT = int(os.environ.get("API_PORT", "8002"))
