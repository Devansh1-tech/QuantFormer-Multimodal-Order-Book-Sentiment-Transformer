# QuantFormer Backend
### Multimodal Order Book & Sentiment Transformer — Production Backend

QuantFormer is an enterprise-grade financial AI backend integrating Deep Learning (**Temporal Fusion Transformer**), NLP (**FinBERT**), Multimodal Feature Fusion, Streaming (**Apache Kafka**), and Real-Time Financial Feeds (**Yahoo Finance & News APIs**) into a unified platform.

---

## 1. System Architecture

```
                                  ┌──────────────────────────┐
                                  │   Live Data Ingestion    │
                                  ├─────────────┬────────────┤
                                  │Yahoo Finance│  News API  │
                                  └──────┬──────┴─────┬──────┘
                                         │            │
                                         ▼            ▼
                                  ┌──────────────────────────┐
                                  │      Kafka Streaming     │
                                  │  (Disabled / Direct Mode)│
                                  └─────────────┬────────────┘
                                                │
                                                ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    QuantFormer FastAPI Backend                                   │
│                                                                                                  │
│  ┌───────────────────────┐   ┌────────────────────────┐   ┌───────────────────────────────────┐  │
│  │   TFT Model (84.51%)  │   │     FinBERT Model      │   │       QuantFormer Fusion          │  │
│  │  Primary Market Pred  │   │  768-D News Sentiment  │   │   Internal Insight Enrichment     │  │
│  └───────────┬───────────┘   └───────────┬────────────┘   └─────────────────┬─────────────────┘  │
│              │                           │                                  │                    │
│              └───────────────────────────┼──────────────────────────────────┘                    │
│                                          │                                                       │
│                                          ▼                                                       │
│                        ┌───────────────────────────────────┐                                     │
│                        │       Services & REST APIs        │                                     │
│                        │  /health, /market, /news, /predict│                                     │
│                        │  /sentiment, /insight, /dashboard │                                     │
│                        └─────────────────┬─────────────────┘                                     │
└──────────────────────────────────────────┼───────────────────────────────────────────────────────┘
                                           │
                                           ▼
                              ┌─────────────────────────┐
                              │  React / Web Dashboard  │
                              └─────────────────────────┘
```

---

## 2. Core Architectural Decisions

1. **TFT is the Primary Production Prediction Model**:
   - The Temporal Fusion Transformer achieves **84.51%** accuracy on Limit Order Book data.
   - All directional trading predictions (`Down`, `Stable`, `Up`) are generated strictly by TFT.
2. **Internal Fusion Usage**:
   - The Multimodal Fusion model is used **internally** to enrich the AI insight and explainability reasoning.
   - It is never exposed as an independent `BUY`/`SELL`/`UP`/`DOWN` trading signal.
3. **Strict Runtime Data Isolation**:
   - **FI-2010** and **Financial PhraseBank** are training datasets only and are **never** loaded at runtime.
   - Market data comes from Yahoo Finance (cached or HTTP 503 fallback).
   - Financial news comes from live News APIs (cached or fallback message).
4. **Dynamic Stock Symbols**:
   - All market endpoints support dynamic tickers via `?symbol=AAPL`, `?symbol=NVDA`, `?symbol=RELIANCE.NS`, etc.
5. **Dashboard Aggregator API**:
   - `GET /api/v1/dashboard?symbol=AAPL` aggregates market data, news, sentiment, insights, and system status in a single network round-trip.

---

## 3. Directory Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── deps.py                     # FastAPI dependency injection
│   │   └── v1/
│   │       ├── router.py               # Aggregated V1 API router
│   │       └── endpoints/
│   │           ├── health.py           # GET /api/v1/health (telemetry)
│   │           ├── models.py           # GET /api/v1/models (model registry)
│   │           ├── market.py           # GET /api/v1/market?symbol= (Yahoo Finance)
│   │           ├── news.py             # GET /api/v1/news (Live news)
│   │           ├── predict.py          # POST /api/v1/predict (TFT inference)
│   │           ├── sentiment.py        # POST /api/v1/sentiment (FinBERT)
│   │           ├── insight.py          # POST /api/v1/insight (Fusion AI insight)
│   │           ├── explain.py          # POST /api/v1/explain (Explainability)
│   │           └── dashboard.py        # GET /api/v1/dashboard (Aggregator)
│   ├── core/
│   │   ├── config.py                   # Pydantic v2 BaseSettings
│   │   └── logging.py                  # Structured multi-handler logging
│   ├── loaders/
│   │   ├── market_loader.py            # Yahoo Finance fetcher + TTL cache
│   │   └── news_loader.py              # News API fetcher + TTL cache
│   ├── models/
│   │   └── model_manager.py            # Singleton ModelManager (TFT, FinBERT, Fusion)
│   ├── schemas/
│   │   ├── common.py                   # API response envelopes
│   │   ├── health.py                   # Health schemas
│   │   ├── market.py                   # Market quote schemas
│   │   ├── news.py                     # News article schemas
│   │   ├── predict.py                  # TFT prediction schemas
│   │   ├── sentiment.py                # FinBERT sentiment schemas
│   │   ├── insight.py                  # Multimodal insight schemas
│   │   ├── explain.py                  # Explainability schemas
│   │   └── dashboard.py                # Dashboard schemas
│   ├── services/
│   │   ├── market_service.py           # Market business logic
│   │   ├── news_service.py             # News business logic
│   │   ├── prediction_service.py       # TFT inference pipeline
│   │   ├── sentiment_service.py        # FinBERT sentiment & explanations
│   │   ├── insight_service.py          # Multimodal synthesis
│   │   ├── explain_service.py          # Reasoning engine
│   │   └── dashboard_service.py        # Aggregator orchestrator
│   ├── kafka/
│   │   ├── config.py                   # Kafka topic configuration
│   │   ├── producer.py                 # Resilient producer
│   │   ├── consumer.py                 # Background daemon consumer
│   │   └── streaming_service.py        # Kafka orchestrator
│   ├── utils/
│   │   ├── constants.py                # Class names, trend mappings, matrices
│   │   └── helpers.py                  # Hardware probes, latency timers
│   └── main.py                         # FastAPI app entry point
├── tests/
│   ├── conftest.py                     # Pytest fixtures & mocks
│   ├── test_health.py                  # Health tests
│   ├── test_models.py                  # Models registry tests
│   ├── test_market.py                  # Market data tests
│   ├── test_news.py                    # News tests
│   ├── test_predict.py                 # Prediction tests
│   ├── test_sentiment.py               # Sentiment tests
│   ├── test_insight.py                 # Insight tests
│   ├── test_explain.py                 # Explainability tests
│   ├── test_dashboard.py               # Dashboard tests
│   ├── test_kafka_disabled.py          # Kafka disabled mode tests
│   ├── test_invalid_input.py           # Input validation tests
│   └── test_missing_models.py          # Degraded model tests
├── logs/                               # Rotating log files
│   ├── backend.log
│   ├── prediction.log
│   └── error.log
├── requirements.txt                    # Backend dependencies
├── .env.example                        # Environment variable template
└── README.md                           # Documentation
```

---

## 4. Quick Start

### 1. Installation

```bash
# Clone and enter directory
cd "Quant Former"

# Install backend dependencies
pip install -r backend/requirements.txt
```

### 2. Configuration

Copy `.env.example` to `.env` inside `backend/`:

```bash
cp backend/.env.example backend/.env
```

Key environment variables:
- `DEFAULT_SYMBOL`: Default stock ticker (e.g. `AAPL`)
- `NEWS_API_KEY`: API key from [newsapi.org](https://newsapi.org)
- `KAFKA_ENABLED`: Set to `true` to enable Kafka streaming (default: `false` for local mode)

### 3. Run the Server

```bash
uvicorn backend.app.main:app --reload
```

The interactive API documentation is available at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 5. API Reference

### Health & Telemetry
- `GET /` — Project overview and endpoint sitemap
- `GET /api/v1/health` — Complete backend, model, GPU, CPU, RAM, and Kafka telemetry
- `GET /api/v1/models` — Loaded model registry, architectures, and checkpoints

### Live Data
- `GET /api/v1/market?symbol=AAPL` — Live Yahoo Finance quote with OHLCV data
- `GET /api/v1/news?limit=10&query=finance` — Latest financial news headlines

### AI Inference
- `POST /api/v1/predict` — TFT market prediction on `(100, 143)` LOB sequence
- `POST /api/v1/sentiment` — FinBERT news sentiment analysis
- `POST /api/v1/insight` — Multimodal AI insight (TFT + FinBERT + Fusion)
- `POST /api/v1/explain` — Prediction explainability with human-readable reasoning

### Dashboard
- `GET /api/v1/dashboard?symbol=AAPL` — Complete aggregated payload for React UI

---

## 6. Running Tests

Execute the full 22-test automated test suite:

```bash
pytest backend/tests/ -v
```

---

## 7. Logging & Monitoring

Logs are written with automatic rotation to `backend/logs/`:
- **`backend.log`**: Application lifecycle, dependency startup, and general events.
- **`prediction.log`**: Dedicated log for AI inference events, confidence, and latency.
- **`error.log`**: High-priority exceptions and error traces only.
