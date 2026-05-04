import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader
from typing import Dict, Any
from src.api.schemas import AnalyzeRequest, AnalyzeResponse
from config.settings import STATIC_API_KEY

from src.auth.dependencies import get_current_user
from src.auth.models import User
from fastapi import Request

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def get_authorized_user(
    request: Request,
    api_key: str = Security(api_key_header)
) -> User:
    from config.settings import USE_AUTH, USE_API_KEY_FALLBACK, STATIC_API_KEY
    
    # Bypass mechanism explicitly natively structurally safely
    if not USE_AUTH:
        return User(user_id="bypass", username="bypass_user", hashed_password="", role="admin", is_active=True)
        
    auth_header = request.headers.get("Authorization")
    
    # 1. Fallback mechanism
    if USE_API_KEY_FALLBACK and not auth_header and api_key == STATIC_API_KEY:
        return User(user_id="fallback", username="api_key_user", hashed_password="", role="admin", is_active=True)
        
    # 2. JWT Mechanism
    return get_current_user(auth_header.split(" ")[1] if auth_header else "")

# Migrated dynamically to new isolated services architecture
from src.services.analyzer_service import AnalyzerService

router = APIRouter()
analyzer_service = AnalyzerService()

from src.middleware.rate_limiter import limiter, ANALYZE_LIMIT

@router.post("/analyze", response_model=AnalyzeResponse)
@limiter.limit(ANALYZE_LIMIT)
async def analyze_kpi(request: Request, body_request: AnalyzeRequest, user: User = Depends(get_authorized_user)):
    try:
        from config.settings import USE_ADVANCED_GUARDRAILS
        safe_query = request.query
        
        if USE_ADVANCED_GUARDRAILS:
            from src.guardrails.input_guardrails import validate_input, InputGuardrailException
            try:
                safe_query = validate_input(body_request.query)
            except InputGuardrailException as ge:
                raise HTTPException(status_code=400, detail=str(ge))

        # Inject structured intent bounds natively seamlessly natively cleanly smartly intuitively fluently purely fluently
        structured_intent_dict = body_request.structured_intent.model_dump(exclude_unset=True) if body_request.structured_intent else {}
        structured_intent_dict["user_role"] = user.role

        # Orchestrate execution via Analyzer Service
        result = await analyzer_service.process_query(
            raw_query=safe_query,
            structured_intent=structured_intent_dict
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
