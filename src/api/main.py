from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.core.sql_generator import generate_sql
from src.core.mlflow_tracker import init_mlflow, log_generation

app = FastAPI(title="QueryForge", version="0.1.0")


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    sql: str
    model: str
    input_tokens: int
    output_tokens: int


class FeedbackRequest(BaseModel):
    question: str
    generated_sql: str
    is_correct: bool
    corrected_sql: str | None = None
    notes: str | None = None


@app.on_event("startup")
async def startup():
    init_mlflow()


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/generate-sql", response_model=QueryResponse)
async def generate(request: QueryRequest):
    try:
        result = generate_sql(request.question)
        log_generation(**result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/feedback")
async def feedback(request: FeedbackRequest):
    # TODO: Store feedback in Delta table for fine-tuning loop
    return {"status": "recorded", "question": request.question}
