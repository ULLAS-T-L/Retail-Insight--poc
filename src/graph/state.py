from typing import Dict, Any, TypedDict, Optional, List

class AgentState(TypedDict, total=False):
    """
    Core state object for LangGraph orchestration cleanly separating boundaries natively.
    """
    # Inputs
    query: str
    session_id: str
    
    # Processed logic
    parsed_intent: Optional[Dict[str, Any]]
    sql_template_used: Optional[str]
    
    # Contexts
    kpi_data: Optional[List[Dict[str, Any]]]
    episodic_history: Optional[List[Dict[str, Any]]]
    semantic_context: str
    compliance_context: str
    
    # Outputs
    analysis: Optional[Dict[str, Any]]
    compliance_flags: Optional[List[str]]
    error: Optional[str]
