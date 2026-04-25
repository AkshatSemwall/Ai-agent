from fastapi import APIRouter, HTTPException
from backend.agent.simple_agent import run_agent
from backend.core.schemas import AnalyzeRequest, AnalyzeResponse
from backend.core.logger import logger

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest) -> dict:
    try:
        return run_agent(payload.query)
    except Exception:
        logger.exception("Failed to process /analyze request")
        raise HTTPException(
            status_code=500,
            detail="Internal error while processing the analysis request.",
        )
