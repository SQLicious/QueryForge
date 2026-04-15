import anthropic
from src.core.config import settings

SYSTEM_PROMPT = """You are a SQL expert for financial databases. Given a natural language question
and schema context, generate valid SQL.

Rules:
- Output ONLY the SQL query, no explanation
- Use standard SQL compatible with Spark SQL / Delta Lake
- Never use DELETE, DROP, TRUNCATE, or any DDL/DML that modifies data
- Always qualify column names with table aliases when joining

Available schemas:

TABLE accounts (
    account_id STRING,
    customer_name STRING,
    account_type STRING,  -- 'checking', 'savings', 'loan', 'credit'
    balance DECIMAL(18,2),
    open_date DATE,
    branch_code STRING,
    status STRING  -- 'active', 'closed', 'frozen'
)

TABLE transactions (
    txn_id STRING,
    account_id STRING,
    txn_date TIMESTAMP,
    amount DECIMAL(18,2),
    txn_type STRING,  -- 'credit', 'debit'
    category STRING,
    description STRING
)

TABLE risk_metrics (
    account_id STRING,
    metric_date DATE,
    credit_score INT,
    risk_rating STRING,  -- 'low', 'medium', 'high', 'critical'
    probability_of_default DECIMAL(5,4),
    loss_given_default DECIMAL(5,4)
)

TABLE model_inventory (
    model_id STRING,
    model_name STRING,
    model_type STRING,
    deployment_date DATE,
    owner STRING,
    status STRING,  -- 'active', 'retired', 'validation'
    last_validation_date DATE
)
"""

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)


def generate_sql(question: str) -> dict:
    response = client.messages.create(
        model=settings.model_name,
        max_tokens=settings.max_tokens,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Generate SQL for: {question}",
            }
        ],
    )
    sql = response.content[0].text.strip()
    # Strip markdown code fences if present
    if sql.startswith("```"):
        lines = sql.split("\n")
        sql = "\n".join(lines[1:-1]).strip()

    return {
        "question": question,
        "sql": sql,
        "model": settings.model_name,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }
