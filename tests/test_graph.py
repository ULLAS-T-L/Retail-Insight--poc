import pytest
from unittest.mock import patch
from src.graph.workflow import compile_workflow

@pytest.fixture
def graph():
    return compile_workflow()

@patch('src.agents.llm_analyzer.LLMAnalyzer.analyze')
@patch('src.data.query_runner.QueryRunner.run_template')
def test_langgraph_compliance_routing(mock_run_template, mock_analyze, graph):
    # Mock LLM to test pure graph traversal unconditionally efficiently
    mock_run_template.return_value = [{"brand": "AlphaBrand", "distribution": 40}]
    mock_analyze.return_value = {
        "summary": "Mocked test summary",
        "drivers": [],
        "risks": [],
        "actions": []
    }
    
    # Execute node exactly dynamically matching compliance limits
    initial_state = {
        "query": "Check compliance violations for AlphaBrand.",
        "session_id": "test_graph_session",
        "parsed_intent": {"brand": "AlphaBrand", "query_type": "compliance_check"}
    }
    
    final_state = graph.invoke(initial_state)
    
    # Evaluates whether the graph traversed RAG dynamically effectively properly accurately.
    assert "workflow_path" in final_state
    assert "compliance_check" in final_state["workflow_path"]
    assert final_state["rag_used"] is True
