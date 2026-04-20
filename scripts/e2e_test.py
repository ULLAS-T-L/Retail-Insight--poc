import urllib.request
import json
import time

URL = "http://127.0.0.1:8000/analyze"
SESSION_ID = "smoke_test_session_ab12"

def hit_endpoint(name: str, payload: dict):
    print(f"\n=============================================")
    print(f"TEST: {name}")
    print(f"QUERY: '{payload.get('query', '')}'")
    print(f"=============================================")
    
    req = urllib.request.Request(URL, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    
    start = time.time()
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            print(f"[STATUS 200] - Processed in {time.time() - start:.2f}s")
            
            meta = res_data.get("metadata", {})
            print(f"\n--- METADATA TRACKING ---")
            print(f"Workflow Path       : {meta.get('workflow_path')}")
            print(f"SQL Template Used   : {meta.get('sql_template_used')}")
            print(f"RAG Used?           : {meta.get('rag_used')}")
            print(f"Episodic Mem Used?  : {meta.get('episodic_memory_used')}")
            print(f"Semantic Mem Used?  : {meta.get('semantic_memory_used')}")
            print(f"Session Active      : {meta.get('session_active')}")
            print(f"Compliance Docs Hit?: {meta.get('retrieved_docs_hit')}")
            
            print(f"\n--- ANALYSIS SUMMARY ---")
            print(res_data.get("analysis", {}).get("summary", "N/A"))
            
    except Exception as e:
        print(f"[ERROR] Request Failed: {e}")

payloads = [
    {
        "name": "1. Simple KPI Query",
        "payload": {
            "query": "What is the sales performance for BetaBrand in hypermarkets?",
            "structured_intent": {"brand": "BetaBrand", "channel": "Hypermarket", "query_type": "simple_kpi"}
        }
    },
    {
        "name": "2. Comparison Query",
        "payload": {
            "query": "Compare AlphaBrand versus BetaBrand online sales.",
            "structured_intent": {"brand": "AlphaBrand", "channel": "E-commerce", "query_type": "comparison"}
        }
    },
    {
        "name": "3. Performance Decline Query",
        "payload": {
            "query": "Why did AlphaBrand drop in the South region last week?",
            "structured_intent": {"brand": "AlphaBrand", "region": "South", "query_type": "performance_decline"}
        }
    },
    {
        "name": "4. Compliance Check Query",
        "payload": {
            "query": "Are there any strict compliance distribution violations currently affecting AlphaBrand?",
            "structured_intent": {"brand": "AlphaBrand", "query_type": "compliance_check"}
        }
    },
    {
        "name": "5. Follow-up Query (Memory Evaluation)",
        "payload": {
            "query": "Can you summarize the compliance violations you just mentioned against my recent comparison?",
            "structured_intent": {"brand": "AlphaBrand", "query_type": "simple_kpi"}
        }
    }
]

for item in payloads:
    # Safely inject session id explicitly mapping memory
    item["payload"]["session_id"] = SESSION_ID
    hit_endpoint(item["name"], item["payload"])
    time.sleep(1) # Breathe securely avoiding rate limits slightly
