from src.evaluation.test_dataset import EVALUATION_DATASET
from src.evaluation.metrics import calculate_hit_rate_at_k, calculate_mrr, calculate_context_precision, calculate_context_recall
from src.rag.retriever import retrieve_documents
from config.settings import RAG_TOP_K

def evaluate_rag() -> tuple[list, dict, list]:
    results = []
    failed_cases = []
    
    total_mrr = 0
    total_hit_rate = 0
    total_precision = 0
    total_recall = 0
    
    for tc in EVALUATION_DATASET:
        query = tc["question"]
        expected_doc = tc.get("expected_relevant_doc")
        
        if not expected_doc:
            # Skip queries that aren't expected to hit RAG natively
            continue
            
        # Call actual local retriever
        retrieved_docs = retrieve_documents("compliance_docs", query, top_k=RAG_TOP_K)
        
        hit_rate = calculate_hit_rate_at_k(retrieved_docs, expected_doc, RAG_TOP_K)
        mrr = calculate_mrr(retrieved_docs, expected_doc)
        precision = calculate_context_precision(retrieved_docs, expected_doc)
        recall = calculate_context_recall(retrieved_docs, expected_doc)
        
        total_hit_rate += hit_rate
        total_mrr += mrr
        total_precision += precision
        total_recall += recall
        
        res = {
            "id": tc["id"],
            "query": query,
            "expected_doc": expected_doc,
            "hit_rate": hit_rate,
            "mrr": mrr,
            "precision": precision,
            "recall": recall
        }
        results.append(res)
        
        if hit_rate == 0:
            failed_cases.append({
                "id": tc["id"],
                "question": query,
                "error": f"RAG failed to surface {expected_doc} in top {RAG_TOP_K}"
            })
            
    count = len(results)
    summary = {}
    if count > 0:
        summary = {
            "avg_hit_rate": total_hit_rate / count,
            "avg_mrr": total_mrr / count,
            "avg_precision": total_precision / count,
            "avg_recall": total_recall / count
        }
        
    return results, summary, failed_cases
