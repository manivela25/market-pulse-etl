# 📊 Market Pulse ETL

[![Market Pulse ETL CI](https://github.com/manivela25/market-pulse-etl/actions/workflows/ci.yml/badge.svg)](https://github.com/manivela25/market-pulse-etl/actions/workflows/ci.yml)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Clean](https://img.shields.io/badge/architecture-modular_ETL-success.svg)]()

A modular, production-grade Python ETL pipeline designed to extract cryptocurrency market data, perform strict schema
validation with data hygiene checks, and load structured records into an indexed SQLite relational database.

---

## 🏗️ Architecture & Core Philosophy

The pipeline is built with strict separation of concerns following industry-standard ETL principles:

```text
[CoinGecko REST API]
         │
         ▼ (Extract)
  CryptoMarketClient (requests.Session + Exponential Backoff)
         │
         ▼ (Transform)
  MarketDataTransformer (Pydantic v2 Schema Validation & Normalization)
         │
         ▼ (Load)
  DatabaseManager (SQLite Batch Inserts + Time-Series Indexes)
         │
         ▼
[data/market_pulse.db]
1. Extract Layer (src/extract/client.py)
Leverages persistent requests.Session connections to minimize TCP handshake overhead.

Resilient network recovery using exponential backoff (1s, 2s, 4s...) for transient rate limits (HTTP 429) or connection timeouts.

Encapsulates connection exceptions into domain-specific APIExtractionError.

2. Transform Layer (src/transform/)
Pydantic v2 Models (models.py): Strict typing and field-level validation rules:

Symbol capitalization (e.g., btc ➔ BTC).

Enforces strictly positive pricing (current_price > 0), rejecting corrupted financial records.

Auto-generates timezone-aware UTC timestamps (extracted_at).

Fault-Tolerant Transformation (transformer.py): Invalid individual records are logged and discarded without crashing the execution batch.

3. Load Layer (src/load/database.py & sql/schema.sql)
Automated schema bootstrapping upon startup.

Bulk ingestion via SQLite executemany to minimize disk I/O latency.

High-performance indexing on coin_id and extracted_at for rapid analytical and time-series queries.

📂 Project Directory Structure
Plaintext
market-pulse-etl/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI workflow (automated testing)
├── data/
│   └── market_pulse.db        # Relational SQLite database
├── sql/
│   └── schema.sql             # Table definition and indexes
├── src/
│   ├── extract/
│   │   └── client.py          # API interaction and network resilience
│   ├── transform/
│   │   ├── models.py          # Domain data models & Pydantic rules
│   │   └── transformer.py     # Data hygiene logic
│   └── load/
│       └── database.py        # Database manager and bulk loader
├── tests/
│   ├── test_client.py         # Mocked API client unit tests
│   ├── test_transformer.py    # Schema validation unit tests
│   └── test_database.py       # Isolated database operations via tmp_path
├── main.py                    # ETL pipeline orchestrator
├── show_db.py                 # CLI inspection tool for database records
├── requirements.txt           # Project dependencies
└── PROJECT_BOARD.md           # Engineering notes & mental model guide
🚀 Quickstart & Setup
1. Clone the Repository
Bash
git clone [https://github.com/manivela25/market-pulse-etl.git](https://github.com/manivela25/market-pulse-etl.git)
cd market-pulse-etl
2. Environment Setup
Bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
3. Run the Pipeline
Extract, validate, and load real-time market data:

Bash
python main.py
4. Inspect Ingested Records
Format and display saved data directly in your terminal:

Bash
python show_db.py
🧪 Automated Testing & CI
The project features a 100% passing test suite across all layers:

Extract Testing: Uses pytest-mock to test network retry behaviors without real API calls or quota consumption.

Transform Testing: Verifies schema guards and boundary conditions (e.g., negative prices, empty payloads).

Load Testing: Employs Pytest's tmp_path fixture to spin up temporary SQLite instances, guaranteeing zero pollution of the actual database.

Run the test suite locally:

Bash
pytest -v
All pushes and pull requests trigger automated validation across isolated Ubuntu runners via GitHub Actions (.github/workflows/ci.yml).