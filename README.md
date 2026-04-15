# QueryForge

Production-grade natural language to SQL engine for financial data — built from first principles with LLMOps discipline.

QueryForge is the production-grade version of what Databricks Genie, Snowflake Cortex Analyst, and Azure AI Foundry's NL2SQL feature are commercializing. It converts natural language questions into validated SQL across multiple financial data schemas, with prompt versioning via MLflow, automated RAGAS evaluation on every GitHub commit, query result validation, and a feedback loop for continuous improvement.

Inspired by the text-to-SQL POC built at SMBC on real banking data.

## Architecture

```
                    +---------------------+
                    |   Natural Language   |
                    |      Question        |
                    +----------+----------+
                               |
                    +----------v----------+
                    |      FastAPI         |
                    |  /generate-sql      |
                    |  /execute           |
                    |  /feedback          |
                    +----------+----------+
                               |
              +----------------+----------------+
              |                                 |
   +----------v----------+           +----------v----------+
   |    Claude API        |           |  Databricks CE       |
   | Chain-of-thought     |           |  Delta Tables:       |
   | reasoning + SQL gen  |           |  - accounts          |
   +----------+----------+           |  - transactions       |
              |                       |  - risk_metrics       |
              |                       |  - model_inventory    |
   +----------v----------+           +---------------------+
   |   Query Validation   |
   +----------+----------+
              |
   +----------v----------+
   |   RAGAS Evaluation   |
   | Faithfulness         |
   | Answer relevancy     |
   | Context recall       |
   +----------+----------+
              |
   +----------v----------+
   |   MLflow Tracking    |
   |  (Databricks CE)     |
   +---------------------+
```

## LLMOps Layer (MLflow + Databricks CE)

- **MLflow Prompt Registry** — Version-controlled prompt templates (system prompt, schema context, few-shot examples)
- **MLflow Experiments** — Every evaluation run logged with SQL accuracy, execution rate, RAGAS scores
- **MLflow Model Registry** — `production` vs `staging` prompt versions, with promotion gates
- **Databricks CE Notebooks** — Schema introspection, Delta table setup, Gold layer sample queries for few-shot context

## Storage Layer (Delta Tables on Databricks CE)

- **Delta Lake** — ACID-compliant storage for all financial schemas
- **Four core tables** — `accounts`, `transactions`, `risk_metrics`, `model_inventory`
- **Setup notebook** — `notebooks/01_setup_delta_tables.py` creates and seeds all tables

## Inference + Evaluation Layer (Docker)

- **FastAPI** — `/generate-sql`, `/execute`, `/feedback` endpoints
- **Claude API** — SQL generation with chain-of-thought reasoning before outputting SQL
- **RAGAS** — Automated evaluation: faithfulness, answer relevancy, context recall
- **GitHub Actions** — Evaluation pipeline runs on every PR, blocks merge if accuracy drops

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Anthropic API key
- Databricks Community Edition account (free)
- Python 3.11+

### Setup

```bash
# Clone the repo
git clone https://github.com/SQLicious/QueryForge.git
cd QueryForge

# Set environment variables
cp .env.example .env
# Add your ANTHROPIC_API_KEY and DATABRICKS_TOKEN to .env
```

### Databricks CE Setup

1. Sign up at [Databricks Community Edition](https://community.cloud.databricks.com)
2. Import `notebooks/01_setup_delta_tables.py` as a notebook
3. Attach to a cluster and run all cells — creates the `queryforge` database with Delta tables
4. Generate a personal access token: User Settings > Developer > Access Tokens

### Run Locally

```bash
# Start the API server
docker-compose up -d

# Run evaluation
python scripts/evaluate.py
```

## Project Structure

```
QueryForge/
├── src/
│   ├── api/              # FastAPI endpoints
│   │   └── main.py
│   ├── core/             # Business logic
│   │   ├── config.py     # Settings and env vars
│   │   ├── sql_generator.py  # Claude-powered NL2SQL
│   │   └── mlflow_tracker.py # MLflow experiment logging
│   └── eval/             # Evaluation framework
│       └── evaluator.py  # RAGAS + accuracy benchmarks
├── notebooks/            # Databricks CE notebooks
│   └── 01_setup_delta_tables.py
├── tests/                # Test suite
├── scripts/              # CLI utilities
│   └── evaluate.py
├── docker-compose.yml    # API service orchestration
├── Dockerfile
├── requirements.txt      # Python dependencies
└── .github/workflows/    # CI/CD pipelines
```

## License

MIT
