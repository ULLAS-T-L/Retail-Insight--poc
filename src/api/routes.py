import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader
from typing import Dict, Any
from src.api.schemas import AnalyzeRequest, AnalyzeResponse
from config.settings import STATIC_API_KEY

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header)):
    if not api_key_header or api_key_header != STATIC_API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials locally gracefully cleanly.")
    return api_key_header

# Migrated dynamically to new isolated services architecture
from src.services.analyzer_service import AnalyzerService

router = APIRouter()
analyzer_service = AnalyzerService()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_kpi(request: AnalyzeRequest, api_key: str = Depends(get_api_key)):
    try:
        from config.settings import USE_ADVANCED_GUARDRAILS
        safe_query = request.query
        
        if USE_ADVANCED_GUARDRAILS:
            from src.guardrails.input_guardrails import validate_input, InputGuardrailException
            try:
                safe_query = validate_input(request.query)
            except InputGuardrailException as ge:
                raise HTTPException(status_code=400, detail=str(ge))

        # Orchestrate execution via Analyzer Service
        result = analyzer_service.process_query(
            raw_query=safe_query,
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
