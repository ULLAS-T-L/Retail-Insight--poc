from typing import Dict, Any, List, Tuple
from src.evaluation.test_dataset import EVALUATION_DATASET
from src.evaluation.metrics import keyword_answer_groundedness
from src.graph.workflow import compile_workflow

def evaluate_agent() -> Tuple[List[Dict[str, Any]], Dict[str, Any], List[Dict[str, Any]]]:
    """Runs the full LangGraph workflow against test cases to measure routing and generation accuracy."""
    app = compile_workflow()
    
    results = []
    failed_cases = []
    
    total_route_accuracy = 0
    total_sql_accuracy = 0
    total_groundedness = 0
    
    # Simple memory bypass dictionary purely for independent agent testing
    test_session = "eval_session_001"
    
    for tc in EVALUATION_DATASET:
        # Pass test case query into graph
        initial_state = {
            "query": tc["question"],
            "session_id": test_session,
            "parsed_intent": {}
        }
        
        try:
            final_state = app.invoke(initial_state)
            
            # Check route accuracy (did it traverse the expected path?)
            workflow_path = final_state.get("workflow_path", "")
            route_match = 1 if tc["expected_query_type"] in workflow_path else 0
            
            # Check SQL template accuracy
            sql_used = final_state.get("sql_template_used", "")
            sql_match = 1 if tc["expected_sql_template"] == sql_used else 0
            
            # Check groundedness of the final answer text
            answer_text = final_state.get("analysis", {}).get("summary", "")
            groundedness = keyword_answer_groundedness(answer_text, tc["expected_answer_keywords"])
            
            total_route_accuracy += route_match
            total_sql_accuracy += sql_match
            total_groundedness += groundedness
            
            res = {
                "id": tc["id"],
                "route_match": route_match,
                "sql_match": sql_match,
                "groundedness": groundedness
            }
            results.append(res)
            
            if route_match == 0 or sql_match == 0:
                failed_cases.append({
                    "id": tc["id"],
                    "question": tc["question"],
                    "error": f"Agent routing mismatch. Expected {tc['expected_query_type']} and {tc['expected_sql_template']}. Got {workflow_path} with {sql_used}."
                })
                
        except Exception as e:
            failed_cases.append({
                "id": tc["id"],
                "question": tc["question"],
                "error": f"Graph invocation threw exception: {str(e)}"
            })
            
    count = len(EVALUATION_DATASET)
    summary = {}
    if count > 0:
        summary = {
            "avg_route_accuracy": total_route_accuracy / count,
            "avg_sql_template_accuracy": total_sql_accuracy / count,
            "avg_groundedness": total_groundedness / count
        }
        
    return results, summary, failed_cases
