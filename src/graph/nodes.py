from typing import Dict, Any
from src.agents.intent_parser import RuleBasedIntentParser
from src.data.db import DatabaseWrapper
from src.data.query_runner import QueryRunner
from src.memory.manager import get_context
from src.rag.compliance_retriever import retrieve_compliance_context
from src.agents.llm_analyzer import LLMAnalyzer
from src.agents.analyzer import DeterministicAnalyzer

# Initialize singletons for simplicity securely natively globally
intent_parser = RuleBasedIntentParser()
db_wrapper = DatabaseWrapper()
query_runner = QueryRunner(db_wrapper)
deterministic_analyzer = DeterministicAnalyzer()

def parse_intent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Extracts mathematical boundaries optionally leveraging early memory bounds."""
    query = state.get("query", "")
    session_id = state.get("session_id", "default_session")
    
    # Fetch Persistent User Memory dynamically
    mem_context = get_context(session_id, query)
    
    # Maintain robust rule-based parsing initially
    parsed_intent = intent_parser.parse(query, None)
    
    return {
        "parsed_intent": parsed_intent,
        "episodic_history": mem_context.get("episodic_history", []),
        "semantic_context": mem_context.get("semantic_context", "")
    }

def retrieve_kpi_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Fetches SQL parameters statically mapping natively."""
    parsed_intent = state.get("parsed_intent")
    sql_template = parsed_intent["sql_template"]
    
    try:
        results = query_runner.run_template(sql_template, parsed_intent["template_params"])
        return {
            "sql_template_used": sql_template,
            "kpi_data": results
        }
    except Exception as e:
        return {"error": f"Database resolution crashed conditionally bounds: {str(e)}"}

def retrieve_compliance_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Conditionally routes boundaries fetching strict RAG embeddings limits seamlessly."""
    query = state.get("query", "")
    
    # Native explicit chromadb extraction limits mapped
    strict_context = retrieve_compliance_context(query)
    
    return {"compliance_context": strict_context}

def compliance_check_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluates rule bounds securely against active quantitative extractions gracefully."""
    results = state.get("kpi_data", [])
    parsed_intent = state.get("parsed_intent", {})
    query_type = parsed_intent.get("query_type", "")
    
    flags = []
    if query_type == "compliance_check" or "performance" in query_type:
        for row in results:
            dist = row.get("distribution", 0)
            if dist < 60:
                flags.append(f"CRITICAL RAG RULE: {row.get('brand', 'Unknown')} distribution at {dist}% falls strictly below rigid bounds.")
                
    return {"compliance_flags": flags}

def generate_answer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Fuses all context vectors and SQL metrics perfectly invoking GenAI structurally accurately."""
    kpi_data = state.get("kpi_data", [])
    parsed = state.get("parsed_intent", {})
    compliance = state.get("compliance_context", "")
    episodic = state.get("episodic_history", [])
    query_type = parsed.get("query_type", "simple_kpi")
    
    # Fusing local memory bounds seamlessly ensuring contexts are retained across spans
    fused_intent = parsed.copy()
    if compliance:
        fused_intent["compliance_constraints_RAG"] = compliance
    if episodic:
        fused_intent["recent_memory_SQLite"] = episodic
        
    try:
        analysis_result = LLMAnalyzer.analyze(query_type, kpi_data, fused_intent)
        if not all(k in analysis_result for k in ("summary", "drivers", "actions", "risks")):
            raise ValueError("LLM safely bypassed incomplete strictly typed JSON schema parameters natively.")
    except Exception as e:
        analysis_result = deterministic_analyzer.analyze(query_type, kpi_data, parsed)
        
    return {"analysis": analysis_result}
