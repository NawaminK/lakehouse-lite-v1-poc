import os
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text

from app.sql_guardrails import SqlValidationError, validate_sql

TRINO_URI = os.getenv("TRINO_URI", "trino://admin@trino:8080/iceberg/gold")
MAX_ROWS = int(os.getenv("MAX_ROWS", "200"))

app = FastAPI(title="Lakehouse AI Query API", version="0.1.0")
engine = create_engine(TRINO_URI)

class QueryRequest(BaseModel):
    sql: str

class QueryResponse(BaseModel):
    row_count: int
    rows: list[dict[str, Any]]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest) -> QueryResponse:
    try:
        sql = validate_sql(req.sql)
    except SqlValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = [dict(row._mapping) for row in result.fetchmany(MAX_ROWS)]

    return QueryResponse(row_count=len(rows), rows=rows)
