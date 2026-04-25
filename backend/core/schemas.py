from typing import List
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    query: str = Field(..., description="User research query")


class AnalyzeResponse(BaseModel):
    query: str = Field(..., description="Original user query")
    summary: str = Field(..., description="Concise research summary")
    key_points: List[str] = Field(..., description="Bullet-point key findings")
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Estimated confidence score between 0 and 1"
    )
