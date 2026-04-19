import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from src.api.schemas import AnalyzeRequest, AnalyzeResponse

# Migrated dynamically to new isolated services architecture
from src.services.analyzer_service import AnalyzerService

router = APIRouter()
analyzer_service = AnalyzerService()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_kpi(request: AnalyzeRequest):
    try:
        # Orchestrate execution via Analyzer Service
        result = analyzer_service.process_query(
            raw_query=request.query,
            structured_intent=request.structured_intent.model_dump(exclude_unset=True) if request.structured_intent else None
        )

        return AnalyzeResponse(
            parsed_intent=result["parsed_intent"],
            sql_template_used=result["sql_template_used"],
            kpi_data=result["kpi_data"],
            analysis=result["analysis"],
            compliance_flags=result["compliance_flags"],
            metadata=result.get("metadata")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
