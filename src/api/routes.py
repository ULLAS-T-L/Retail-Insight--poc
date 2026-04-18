from fastapi import APIRouter, HTTPException
from src.api.schemas import AnalyzeRequest, AnalyzeResponse, AnalysisResult
from src.api.services import KPIService

router = APIRouter()
kpi_service = KPIService()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_query(request: AnalyzeRequest):
    """
    1. Parse the user's intent to extract entities (or accept structured JSON).
    2. Obtain the relevant SQL template via the Service Layer.
    3. Execute the SQL safely using parameterized rules.
    4. Run rule-based analysis returning deterministic summaries, drivers, and actions.
    """
    if not request.query and not request.structured_intent:
        raise HTTPException(status_code=400, detail="Must provide 'query' or 'structured_intent'.")

    try:
        req_structured = request.structured_intent.model_dump() if request.structured_intent else None
        response_data = kpi_service.analyze(request.query, req_structured)
        
        # Type verification using Pydantic
        analysis_obj = AnalysisResult(**response_data["analysis"])
        
        return AnalyzeResponse(
            parsed_intent=response_data["parsed_intent"],
            sql_template_used=response_data["sql_template_used"],
            kpi_data=response_data["kpi_data"],
            analysis=analysis_obj,
            compliance_flags=response_data["compliance_flags"]
        )
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
