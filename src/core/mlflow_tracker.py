import mlflow
from src.core.config import settings


def init_mlflow():
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_experiment(settings.mlflow_experiment_name)


def log_generation(question: str, sql: str, model: str, input_tokens: int, output_tokens: int):
    with mlflow.start_run(nested=True):
        mlflow.log_params({
            "model": model,
            "question_length": len(question),
        })
        mlflow.log_metrics({
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
        })
        mlflow.log_text(question, "question.txt")
        mlflow.log_text(sql, "generated_sql.sql")


def log_evaluation(metrics: dict, prompt_version: str):
    with mlflow.start_run(nested=True):
        mlflow.log_param("prompt_version", prompt_version)
        mlflow.log_metrics(metrics)
