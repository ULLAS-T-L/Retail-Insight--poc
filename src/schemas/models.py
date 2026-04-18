from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class AnalyzeRequest(BaseModel):
    query: str = Field(..., description="The user's question or intent")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Optional extra context data")

class AnalyzeResponse(BaseModel):
    intent: str = Field(description="The matched template intent")
    sql: str = Field(description="The compiled SQL query used")
    results: List[Dict[str, Any]] = Field(description="Structured JSON results from the database")
