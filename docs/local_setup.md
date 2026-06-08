# Local Setup — AI Fraud Detection Platform

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.11+ | `python --version` to check |
| UV | latest | `pip install uv` or see [uv docs](https://docs.astral.sh/uv/) |
| Docker + Docker Compose | latest | For Redis and Neo4j |
| Neo4j | 5.x | Via Docker (recommended) or standalone |
| Redis | 7.x | Via Docker (recommended) or standalone |

---

## 1. Clone and Navigate

```bash
git clone https://github.com/anil-avvaru-cool/ai-fraud-detection-platform.git
cd ai-fraud-detection-platform
```

---

## 2. Environment Variables

Copy the example env file and fill in required values:

```bash
cp example.env .env
```

Required variables:

```bash
# Infra — must be set, no defaults
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password_here
REDIS_URL=redis://localhost:6379

# Optional overrides (have sensible defaults)
API_HOST=0.0.0.0
API_PORT=8002
DATA_PLATFORM_ROOT=../insurance-data-platform
```

> **Note**: The app will fail to start if `NEO4J_PASSWORD` is not set.

---

## 3. Start Infrastructure Services

### Via Docker Compose (recommended)

```bash
docker compose up -d
```

This starts:
- **Redis** on port `6379` — online feature store
- **Neo4j** on ports `7474` (browser) and `7687` (Bolt) — fraud graph

Verify services are healthy:

```bash
docker compose ps
```

### Manual (without Docker)

**Redis:**
```bash
redis-server --daemonize yes
redis-cli ping   # should return PONG
```

**Neo4j:**
Download from [neo4j.com/download](https://neo4j.com/download/), set password to match `NEO4J_PASSWORD` in `.env`, then:
```bash
neo4j start
```
Neo4j Browser available at `http://localhost:7474`.

---

## 4. Install Dependencies

```bash
uv sync
```

If `pyproject.toml` is not yet present (transitional — see requirements.txt):
```bash
uv pip install -r requirements.txt
```

The `insurance-data-platform` package (feature store, entity resolution, claims data) is a sibling repo dependency. Clone it at the same directory level:

```bash
cd ..
git clone https://github.com/anil-avvaru-cool/insurance-data-platform.git
cd ai-fraud-detection-platform
```

---

## 5. Run the API Server

```bash
uv run uvicorn api.fraud_score_router:router --host 0.0.0.0 --port 8002 --reload
```

API endpoints:
- `POST /score/sync` — synchronous fraud scoring (<100ms, blocks FNOL)
- `POST /score/async` — asynchronous deep enrichment
- `GET /score/explanation/{claim_id}` — SHAP-based explanation
- `GET /docs` — OpenAPI documentation (Swagger UI)
- `GET /redoc` — ReDoc documentation

---

## 6. Train the Fraud Model

Training requires claims data from `insurance-data-platform`. After running synthetic data generation there:

```bash
uv run python -c "
from pathlib import Path
from fraud_scoring.ensemble.tabular_model import train
metrics = train(
    claims_path=Path('../insurance-data-platform/data/raw/claims.parquet'),
    quotes_path=Path('../insurance-data-platform/data/raw/quotes.parquet'),
    output_dir=Path('models/artifacts'),
)
print(metrics)
"
```

Model artifacts saved to `models/artifacts/` (excluded from git).

---

## 7. Run Tests

```bash
uv run pytest                          # all tests
uv run pytest tests/unit/              # unit tests only
uv run pytest tests/integration/       # integration tests (requires running services)
uv run pytest -k "test_name"           # single test by name
```

---

## 8. Inference Architecture Reference

**Synchronous path (<100ms)** — blocks FNOL submission:

| Component | Budget |
|-----------|--------|
| Redis feature retrieval | ~5ms |
| Device reputation lookup | ~10ms |
| Graph neighborhood query (1–2 hops) | ~20ms |
| Tabular XGBoost scoring | ~5ms |
| Image hash check | ~15ms |
| Decision orchestration | ~10ms |
| **Total** | **~65ms** |

**Asynchronous path** — post-submission: deep ViT image analysis, 3+ hop ring detection, LLM narrative reconciliation.

---

## 9. Decision Tiers

| Score | Threshold | Action |
|-------|-----------|--------|
| Low | < 0.25 | Straight-through processing (STP) |
| Medium | 0.25–0.60 | Request additional evidence |
| High | 0.60–0.85 | SIU referral + payment delay |
| Extreme | > 0.85 | Payment hold + mandatory investigation |

---

## Troubleshooting

**Redis connection refused**
```bash
docker compose ps          # check redis is running
redis-cli -u $REDIS_URL ping
```

**Neo4j authentication failure**
- Confirm `NEO4J_PASSWORD` in `.env` matches the password set in Neo4j (default first-run password is `neo4j`; you must change it on first login).
- Neo4j Browser: `http://localhost:7474`

**`DATA_PLATFORM_ROOT` not found**
- The default path assumes `insurance-data-platform/` is a sibling directory.
- Override with `DATA_PLATFORM_ROOT=/absolute/path/to/insurance-data-platform` in `.env`.

**`NotImplementedError` on API endpoints**
- Most endpoints are stubs planned for Weeks 4–6. Check the [status table in Readme.md](../Readme.md#status).
