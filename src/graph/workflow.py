from langgraph.graph import StateGraph, END
from src.graph.state import AgentState
from src.graph.nodes import (
    parse_intent_node, 
    retrieve_kpi_node,
    retrieve_compliance_node,
    compliance_check_node,
    generate_answer_node
)
from src.graph.router import route_after_kpi, route_after_compliance

def compile_workflow():
    """
    Constructs the operational state graph bounds securely linking nodes and conditionals dynamically cleanly.
    """
    workflow = StateGraph(AgentState)
    
    # Add robust logic nodes natively securely overriding parameters
    workflow.add_node("parse_intent", parse_intent_node)
    workflow.add_node("retrieve_kpi", retrieve_kpi_node)
    workflow.add_node("retrieve_compliance", retrieve_compliance_node)
    workflow.add_node("compliance_check", compliance_check_node)
    workflow.add_node("generate_answer", generate_answer_node)
    
    # Define exact edge routing matrices strictly avoiding infinite loops gracefully
    workflow.set_entry_point("parse_intent")
    
    workflow.add_edge("parse_intent", "retrieve_kpi")
    
    # Branching decision points dynamically assessing active bounds conditionally natively locally 
    workflow.add_conditional_edges(
        "retrieve_kpi",
        route_after_kpi,
        {
            "retrieve_compliance": "retrieve_compliance",
            "generate_answer": "generate_answer"
        }
    )
    
    workflow.add_conditional_edges(
        "retrieve_compliance",
        route_after_compliance,
        {
            "compliance_check": "compliance_check",
            "generate_answer": "generate_answer"
        }
    )
    
    workflow.add_edge("compliance_check", "generate_answer")
    workflow.add_edge("generate_answer", END)
    
    return workflow.compile()
