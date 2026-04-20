from typing import Dict, Any
from src.memory.episodic import store_conversation, get_recent_history
from src.memory.semantic import store_embedding, retrieve_similar_context

def save_turn(session_id: str, user_query: str, agent_response: Dict[str, Any]) -> None:
    """
    Unified mapping gateway. Dispatches explicitly into SQLite (Episodic) and Chroma (Semantic).
    """
    # 1. Linear Conversational Array Tracking
    store_conversation(session_id, user_query, agent_response)
    
    # 2. Extract semantic traits explicitly caching analytical bounds loosely safely
    if agent_response.get("analysis") and "summary" in agent_response.get("analysis", {}):
        semantic_string = f"User asked about: {user_query}. Finding: {agent_response['analysis']['summary']}"
        store_embedding(session_id, semantic_string, {"type": "auto_summary"})

def get_context(session_id: str, query: str) -> Dict[str, Any]:
    """
    Fuses unified memory arrays securely falling back statically smoothly seamlessly if extraction throws.
    """
    try:
        recent = get_recent_history(session_id, limit=3)
    except Exception:
        recent = []
        
    try:
        semantic = retrieve_similar_context(session_id, query)
    except Exception:
        semantic = ""
    
    return {
        "episodic_history": recent,
        "semantic_context": semantic
    }
