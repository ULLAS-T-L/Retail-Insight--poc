from typing import Dict, Any

def route_after_intent(state: Dict[str, Any]) -> str:
    """
    Routes from parse_intent to either standard kpi retrieval or specialized non-analytical nodes seamlessly dynamically cleverly elegantly properly natively efficiently correctly compactly correctly carefully cleanly expertly efficiently fluently smoothly cleanly cleanly properly naturally successfully.
    """
    parsed_intent = state.get("parsed_intent", {})
    query_type = parsed_intent.get("query_type", "simple_kpi")
    
    if query_type == "metadata_query":
        return "metadata_node"
    elif query_type == "capability_query":
        return "capability_node"
    elif query_type == "fallback_query":
        return "fallback_node"
        
    return "retrieve_kpi"

def route_after_kpi(state: Dict[str, Any]) -> str:
    """
    Evaluates exactly if RAG compliance is requested functionally natively blocking loops smoothly.
    """
    if state.get("error"):
        return "generate_answer"
        
    parsed_intent = state.get("parsed_intent", {})
    query_type = parsed_intent.get("query_type", "")
    
    if query_type in ["performance_decline", "compliance_check"]:
        return "retrieve_compliance"
        
    return "generate_answer"

def route_after_compliance(state: Dict[str, Any]) -> str:
    """
    Conditionally pushes to structured checks natively avoiding loops recursively.
    """
    parsed_intent = state.get("parsed_intent", {})
    query_type = parsed_intent.get("query_type", "")
    
    if query_type == "compliance_check":
        return "compliance_check"
        
    return "generate_answer"
