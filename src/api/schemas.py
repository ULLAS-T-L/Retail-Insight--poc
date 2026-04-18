from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class StructuredIntent(BaseModel):
    brand: Optional[str] = None
    region: Optional[str] = None
    channel: Optional[str] = None
    query_type: Optional[str] = Field(None, description="E.g., simple_kpi, comparison, performance_decline, compliance_check")
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    period_1_start: Optional[str] = None
    period_1_end: Optional[str] = None
    period_2_start: Optional[str] = None
    period_2_end: Optional[str] = None
    market_share_threshold: Optional[float] = None
    distribution_threshold: Optional[float] = None

class AnalyzeRequest(BaseModel):
    query: Optional[str] = Field(None, description="The user's free-text question")
    structured_intent: Optional[StructuredIntent] = Field(None, description="Optional structured fields")

class AnalysisResult(BaseModel):
    summary: str = Field(description="A textual summary of the output")
    drivers: List[str] = Field(description="Mathematical anomalies or drivers mapped to the outcome")
    risks: Optional[List[str]] = Field(None, description="Identified risks from the LLM or rules engine")
    actions: List[str] = Field(description="Recommended tactical actions based on the analysis")

class AnalyzeResponse(BaseModel):
    parsed_intent: Dict[str, Any] = Field(description="The final intent parameters used after processing")
    sql_template_used: str = Field(description="The compiled SQL template string")
    kpi_data: List[Dict[str, Any]] = Field(description="Structured JSON results from the database")
    analysis: AnalysisResult = Field(description="Analytical breakdown splitting into summary, drivers, and actionable recommendations")
    compliance_flags: Optional[List[str]] = Field(None, description="Any detected compliance violations (if query_type is compliance_check)")
