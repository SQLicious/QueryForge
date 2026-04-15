"""Quick test: verify MLflow tracks locally."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import mlflow

# Use local file-based tracking (no server needed)
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("queryforge-eval")

with mlflow.start_run(run_name="test-local-tracking"):
    # Simulate what a real eval run would log
    mlflow.log_param("prompt_version", "v1")
    mlflow.log_param("model", "claude-sonnet-4-20250514")

    mlflow.log_metrics({
        "total_questions": 5,
        "sql_accuracy": 0.80,
        "avg_tokens_per_query": 350,
        "faithfulness": 0.90,
        "answer_relevancy": 0.85,
        "context_recall": 0.78,
    })

    mlflow.log_text("SELECT SUM(balance) FROM accounts WHERE status = 'active'", "sample_sql.sql")
    mlflow.log_text("What is the total balance of active accounts?", "sample_question.txt")

    run_id = mlflow.active_run().info.run_id
    print(f"MLflow run logged successfully!")
    print(f"Run ID: {run_id}")
    print(f"Experiment: queryforge-eval")
    print(f"\nTo view the dashboard, run:")
    print(f"  mlflow ui --backend-store-uri mlruns")
    print(f"  Then open http://localhost:5000")
