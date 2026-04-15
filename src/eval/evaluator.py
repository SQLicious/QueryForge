import mlflow
from src.core.sql_generator import generate_sql
from src.core.mlflow_tracker import init_mlflow, log_evaluation

EVAL_QUESTIONS = [
    {
        "question": "What is the total balance across all active checking accounts?",
        "expected_sql": "SELECT SUM(balance) AS total_balance FROM accounts WHERE account_type = 'checking' AND status = 'active'",
    },
    {
        "question": "Show me the top 10 customers by transaction volume in the last 30 days",
        "expected_sql": "SELECT a.customer_name, COUNT(t.txn_id) AS txn_count FROM accounts a JOIN transactions t ON a.account_id = t.account_id WHERE t.txn_date >= CURRENT_DATE - INTERVAL 30 DAY GROUP BY a.customer_name ORDER BY txn_count DESC LIMIT 10",
    },
    {
        "question": "List all accounts with a high or critical risk rating and balance over 100000",
        "expected_sql": "SELECT a.account_id, a.customer_name, a.balance, r.risk_rating FROM accounts a JOIN risk_metrics r ON a.account_id = r.account_id WHERE r.risk_rating IN ('high', 'critical') AND a.balance > 100000",
    },
    {
        "question": "How many models are currently in validation status?",
        "expected_sql": "SELECT COUNT(*) AS model_count FROM model_inventory WHERE status = 'validation'",
    },
    {
        "question": "What is the average probability of default for each risk rating category?",
        "expected_sql": "SELECT risk_rating, AVG(probability_of_default) AS avg_pd FROM risk_metrics GROUP BY risk_rating ORDER BY avg_pd DESC",
    },
]


def run_evaluation(prompt_version: str = "v1") -> dict:
    init_mlflow()

    results = []
    with mlflow.start_run(run_name=f"eval-{prompt_version}"):
        for item in EVAL_QUESTIONS:
            result = generate_sql(item["question"])
            results.append({
                "question": item["question"],
                "expected_sql": item["expected_sql"],
                "generated_sql": result["sql"],
                "tokens_used": result["input_tokens"] + result["output_tokens"],
            })

        total = len(results)
        metrics = {
            "total_questions": total,
            "total_tokens": sum(r["tokens_used"] for r in results),
            "avg_tokens_per_query": sum(r["tokens_used"] for r in results) / total,
        }
        log_evaluation(metrics, prompt_version)

    return {"prompt_version": prompt_version, "metrics": metrics, "results": results}


if __name__ == "__main__":
    output = run_evaluation()
    for r in output["results"]:
        print(f"\nQ: {r['question']}")
        print(f"Generated: {r['generated_sql']}")
        print(f"Expected:  {r['expected_sql']}")
