from typing import Dict, Any, List, Tuple
from src.evaluation.test_dataset import EVALUATION_DATASET
from src.memory.manager import get_context, save_turn

def evaluate_memory() -> Tuple[List[Dict[str, Any]], Dict[str, Any], List[Dict[str, Any]]]:
    """Evaluates multi-turn memory recall logic by pushing sequences to the memory layer dynamically."""
    
    results = []
    failed_cases = []
    
    total_episodic_hits = 0
    eval_session = "memory_eval_session_001"
    follow_up_count = 0
    
    for tc in EVALUATION_DATASET:
        query = tc["question"]
        is_follow_up = tc.get("is_follow_up", False)
        
        # Step 1: Query memory dynamically
        context = get_context(eval_session, query)
        
        episodic_hit = 1 if context.get("episodic_history") else 0
        semantic_hit = 1 if context.get("semantic_context") else 0
        
        if is_follow_up:
            follow_up_count += 1
            total_episodic_hits += episodic_hit
            
            if episodic_hit == 0:
                failed_cases.append({
                    "id": tc["id"],
                    "question": query,
                    "error": "Follow-up question failed to trigger an episodic history hit dynamically."
                })
        
        # Step 2: Push current question to memory to setup the next turn
        fake_response = {
            "metadata": {"session_active": eval_session, "eval_bypass": True},
            "parsed_intent": {"query": query}
        }
        save_turn(eval_session, query, fake_response)
        
        results.append({
            "id": tc["id"],
            "episodic_hit": episodic_hit,
            "semantic_hit": semantic_hit,
            "is_follow_up": is_follow_up
        })
        
    summary = {}
    if follow_up_count > 0:
        summary = {
            "episodic_context_hit_rate": total_episodic_hits / follow_up_count,
        }
        
    return results, summary, failed_cases
