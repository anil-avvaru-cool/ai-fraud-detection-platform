> **Part of the [Redwood AI Insurance Platform](https://github.com/anil-avvaru-cool/redwood-ai-insurance)**
> — an end-to-end intelligent insurance operations platform spanning underwriting through claims settlement.

# AI Fraud Detection Platform

Ensemble fraud scoring, graph intelligence, and sync/async inference — the adversarial
risk orchestration system at the heart of the Redwood AI claims pipeline.

## Overview

Modern fraud detection is not a supervised classification problem. It is an
adversarial risk orchestration system. Fraud tactics evolve. A model that learns to
replicate past detection also replicates past blind spots.

This platform combines:
- **Ensemble scoring** — XGBoost + Graph Neural Network + NLP Transformer + Vision
  model + Isolation Forest, stacked via a meta-learner
- **Graph intelligence** — Neo4j fraud ring detection, attorney network centrality,
  Louvain community detection on shared attributes
- **Hybrid inference** — synchronous path (<100ms, blocks FNOL) + asynchronous
  path (deep enrichment, post-submission)
- **Investigator Copilot** — HITL workflow with SHAP-based case summaries, graph
  explorer, and dynamic evidence checklists

## Architecture

```
FNOL Intake
      │
      ▼
Real-Time Feature Enrichment  ◄── Feature Store (Redis, sub-10ms)
      │
      ▼
Multi-Signal Fusion
Graph · Device · Policy · Telematics · NLP · Vision
      │
      ▼
Ensemble Fraud Scoring Engine
XGBoost + GNN + NLP + ViT + Anomaly → Stacking Meta-Learner
      │
      ▼
Decision Orchestration
(score tiers + rules + compliance)
      │
      ▼
Adaptive Action Routing
STP (auto) | Evidence Request | SIU Escalation | Payment Hold
      │
      ▼
Investigator Copilot (HITL)
      │
      ▼
Label Store → Retraining
```

## Inference Architecture

**Synchronous path (<100ms)** — blocks FNOL submission:

| Component | Budget |
|---|---|
| Online feature retrieval (Redis) | ~5ms |
| Device reputation lookup | ~10ms |
| Graph neighborhood query (1–2 hops) | ~20ms |
| Tabular XGBoost scoring | ~5ms |
| Lightweight image hash check | ~15ms |
| Decision orchestration + routing | ~10ms |
| **Total** | **~65ms** |

**Asynchronous path** — post-submission enrichment:
Deep ViT image analysis, full graph traversal (3+ hop ring detection), LLM
narrative reconciliation, third-party enrichment.

## Decision Tiers

| Score Tier | Threshold | Action |
|---|---|---|
| Low risk | < 0.25 | Straight-through processing (STP) |
| Medium risk | 0.25–0.60 | Request additional evidence |
| High risk | 0.60–0.85 | SIU referral + payment delay notification |
| Extreme risk | > 0.85 | Payment hold + mandatory manual investigation |

## Status

| Component | Status |
|---|---|
| Feature store integration | 🔨 In progress |
| Tabular XGBoost baseline | 📋 Planned — Week 4 |
| Graph feature enrichment (Neo4j) | 📋 Planned — Week 4 |
| NLP narrative scoring | 📋 Planned — Week 4 |
| Sync/async inference API | 📋 Planned — Week 4 |
| Investigator Copilot | 📋 Planned — Week 5 |
| Champion-Challenger loop | 📋 Planned — Week 6 |

## Roadmap

- **Week 4:** XGBoost baseline + graph features + SHAP explainability + FastAPI sync path
- **Week 5:** Async enrichment pipeline + Investigator Copilot + HITL feedback loop
- **Week 6:** GNN layer + NLP narrative scoring + vision model integration
- **Week 7:** PSI drift monitoring + Champion-Challenger + AWS deployment

## Design Decisions

From the [platform Decision Log](https://github.com/anil-avvaru-cool/redwood-ai-insurance/blob/main/docs/DECISION_LOG.md):

| Decision | Summary |
|---|---|
| DEC-003 | Telematics trio — `telematics_enrolled_but_missing` is a fraud signal, not missing data |
| DEC-005 | Graph features as second-pass — mirrors Neo4j live query at inference time |
| DEC-007 | 33% fraud rate in synthetic data — corrected via `scale_pos_weight`, not data ratio |
| DEC-010 | `risk_score_at_issuance` re-enters fraud scoring — the shared data spine |

## Git Repository Structure

```text
ai-fraud-detection-platform/
├── config.py                          ← tier thresholds, latency budgets, PSI config, Neo4j/Redis
├── requirements.txt
├── .gitignore                         ← data/ explicitly excluded (owned by insurance-data-platform)
│
├── fraud_scoring/
│   ├── ensemble/
│   │   ├── tabular_model.py           ← XGBoost on 20-feature fraud vector
│   │   └── meta_learner.py            ← stacking meta-learner (LR or LightGBM)
│   ├── graph/
│   │   ├── gnn_scorer.py              ← GraphSAGE (async path)
│   │   └── neo4j_client.py            ← sync (1–2 hop) + async (3+ hop) query helpers
│   ├── nlp/
│   │   └── narrative_scorer.py        ← inconsistency + complexity scores
│   ├── vision/
│   │   └── image_scorer.py            ← ViT + CLIP (hash check sync, full ViT async)
│   └── anomaly/
│       └── anomaly_detector.py        ← Isolation Forest / Autoencoder
│
├── decision_engine/
│   ├── orchestrator.py                ← tier routing + adverse action docs
│   ├── rules_engine.py                ← business rules, state DOI constraints
│   └── action_router.py               ← dispatches to STP / evidence / SIU / hold
│
├── inference/
│   ├── sync/
│   │   └── fnol_scorer.py             ← <100ms path, latency budgets documented
│   └── async/
│       └── deep_enrichment.py         ← post-submission enrichment, escalation hook
│
├── explainability/
│   ├── shap_explainer.py              ← top-5 SHAP + counterfactuals + adverse action
│   └── graph_explainer.py             ← fraud ring path → human-readable explanation
│
├── monitoring/
│   ├── psi_drift/
│   │   └── score_drift.py             ← score + feature PSI, keyed on fnol_submitted_at
│   ├── shap/
│   │   └── shap_monitor.py            ← SHAP snapshot write + drift comparison
│   └── champion_challenger/
│       └── cc_framework.py            ← shadow → Gini check → phased rollout → promote
│
├── investigator_copilot/
│   ├── case_summary.py                ← auto-generated case brief, evidence checklist
│   └── feedback_loop.py               ← confirms/clears/escalates → label store
│
├── adversarial/
│   └── red_team_pipeline.py           ← synthetic identities, image spoofing, ring sim
│
├── api/
│   ├── fraud_score_router.py          ← FastAPI: /score/sync, /score/async, /explanation
│   └── schemas.py                     ← Pydantic schemas (DEC-009: no standalone JSON Schema)
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── docs/                              ← architecture diagrams, sync/async latency table
└── scripts/
```