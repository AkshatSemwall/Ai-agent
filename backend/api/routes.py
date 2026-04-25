from fastapi import APIRouter
from backend.agent.simple_agent import run_agent

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/analyze")
def analyze(query: str):
    return run_agent(query)