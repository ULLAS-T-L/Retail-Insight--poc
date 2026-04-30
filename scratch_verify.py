import asyncio
from src.graph.workflow import compile_workflow

graph = compile_workflow()

def test_intent(query: str):
    print(f"\\n--- Testing Query: '{query}' ---")
    initial_state = {
        "query": query,
        "session_id": "test_session",
        "user_role": "admin"
    }
    final_state = graph.invoke(initial_state)
    
    print(f"Intent Parsed: {final_state.get('parsed_intent', {}).get('query_type')}")
    print(f"Workflow Path: {final_state.get('workflow_path')}")
    
    analysis = final_state.get('analysis', {})
    if 'summary' in analysis:
        print(f"Response Summary: {analysis['summary']}")
    else:
        print("Response: ", analysis)

if __name__ == "__main__":
    queries = [
        "What brands do you have?",
        "What can I ask?",
        "Why is the sky blue?"
    ]
    
    for q in queries:
        test_intent(q)
