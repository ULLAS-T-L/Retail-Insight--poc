from typing import List, Dict, Any

def calculate_hit_rate_at_k(retrieved_docs: List[Dict[str, Any]], expected_doc: str, k: int = 3) -> int:
    """Checks if the expected_doc is within the top K retrieved documents."""
    if not expected_doc:
        return 1 if not retrieved_docs else 0 # Expected no docs
        
    for doc in retrieved_docs[:k]:
        metadata = doc.get("metadata") or {}
        source = metadata.get("source", "")
        if expected_doc in source:
            return 1
    return 0

def calculate_mrr(retrieved_docs: List[Dict[str, Any]], expected_doc: str) -> float:
    """Calculates Mean Reciprocal Rank."""
    if not expected_doc:
        return 1.0 if not retrieved_docs else 0.0
        
    for i, doc in enumerate(retrieved_docs):
        metadata = doc.get("metadata") or {}
        source = metadata.get("source", "")
        if expected_doc in source:
            return 1.0 / (i + 1)
    return 0.0

def calculate_context_precision(retrieved_docs: List[Dict[str, Any]], expected_doc: str) -> float:
    """
    Very simplified precision: Out of retrieved docs, how many are the expected doc?
    In a binary relevance local setup, this is mostly 1 / len(retrieved_docs) if hit.
    """
    if not retrieved_docs:
        return 1.0 if not expected_doc else 0.0
        
    if not expected_doc:
        return 0.0
        
    relevant_count = 0
    for doc in retrieved_docs:
        metadata = doc.get("metadata") or {}
        source = metadata.get("source", "")
        if expected_doc in source:
            relevant_count += 1
            
    return relevant_count / len(retrieved_docs)

def calculate_context_recall(retrieved_docs: List[Dict[str, Any]], expected_doc: str) -> float:
    """Simplified recall: Did we retrieve the expected doc at all?"""
    return float(calculate_hit_rate_at_k(retrieved_docs, expected_doc, k=100))

def keyword_answer_groundedness(answer: str, expected_keywords: List[str]) -> float:
    """Calculates what percentage of expected keywords made it into the final response."""
    if not expected_keywords:
        return 1.0
        
    answer_lower = answer.lower()
    hits = sum(1 for kw in expected_keywords if kw.lower() in answer_lower)
    return hits / len(expected_keywords)
