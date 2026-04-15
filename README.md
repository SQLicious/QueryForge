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
   |    Claude API        |           |    PostgreSQL        |
   | Chain-of-thought     |           | Financial schemas:   |
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
   +---------------------+
```

## LLMOps Layer (MLflow + Databricks CE)

- **MLflow Prompt Registry** — Version-controlled prompt templates (system prompt, schema context, few-shot examples)
- **MLflow Experiments** — Every evaluation run logged with SQL accuracy, execution rate, RAGAS scores
- **MLflow Model Registry** — `production` vs `staging` prompt versions, with promotion gates
- **Databricks CE Notebooks** — Schema introspection, Gold layer sample queries for few-shot context

## Inference + Evaluation Layer (Docker)

- **FastAPI** — `/generate-sql`, `/execute`, `/feedback` endpoints
- **PostgreSQL** — Sample financial database (accounts, transactions, risk_metrics, model_inventory schemas)
- **Claude API** — SQL generation with chain-of-thought reasoning before outputting SQL
- **RAGAS** — Automated evaluation: faithfulness, answer relevancy, context recall
- **GitHub Actions** — Evaluation pipeline runs on every PR, blocks merge if accuracy drops

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Anthropic API key
- Python 3.11+

### Setup

```bash
# Clone the repo
git clone https://github.com/SQLicious/QueryForge.git
cd QueryForge

# Set environment variables
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

# Start services
docker-compose up -d

# Run evaluation
python scripts/evaluate.py
```

## Project Structure

```
QueryForge/
├── src/                  # Application source code
├── tests/                # Test suite
├── scripts/              # Utility and evaluation scripts
├── data/                 # Schema definitions and sample data
├── docker-compose.yml    # Service orchestration
├── requirements.txt      # Python dependencies
└── .github/workflows/    # CI/CD pipelines
```

## License

MIT
