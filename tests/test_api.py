import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main import app

client = TestClient(app)

def test_api_health():
    response = client.get("/docs")
    assert response.status_code == 200

@patch('src.agents.llm_analyzer.LLMAnalyzer.analyze')
def test_analyze_endpoint_simple_kpi(mock_analyze):
    # Mock LLM securely so CI/CD doesn't need GEMINI_API_KEY
    mock_analyze.return_value = {
        "summary": "Mocked test summary",
        "drivers": [],
        "risks": [],
        "actions": []
    }
    
    payload = {
        "query": "What is the sales performance for BetaBrand in hypermarkets?",
        "structured_intent": {
            "brand": "BetaBrand",
            "channel": "Hypermarket",
            "query_type": "simple_kpi"
        }
    }
    
    response = client.post(
        "/analyze", 
        json=payload,
        headers={"X-API-KEY": "secure-retail-key-123"}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert data["sql_template_used"] == "kpi_timeseries"
    assert "Mocked test summary" in data["analysis"]["summary"]
    
    # Verify metadata arrays populate seamlessly
    meta = data.get("metadata", {})
    assert "workflow_path" in meta
    assert meta["rag_used"] is False
