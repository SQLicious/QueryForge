from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    databricks_host: str = "https://community.cloud.databricks.com"
    databricks_token: str = ""
    mlflow_tracking_uri: str = "sqlite:///mlflow.db"
    mlflow_experiment_name: str = "queryforge-eval"
    model_name: str = "claude-sonnet-4-20250514"
    max_tokens: int = 1024
    prompt_version: str = "v1"

    class Config:
        env_file = ".env"


settings = Settings()
