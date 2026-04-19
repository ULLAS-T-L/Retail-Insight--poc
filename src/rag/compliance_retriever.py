from typing import List, Dict, Any
from src.rag.retriever import retrieve_documents

def retrieve_compliance_context(query: str, top_k: int = 3) -> str:
    """
    Retrieves strict compliance policy limit clauses locally overriding loose contexts logically.
    Returns concatenated compact constraints matching active arrays semantic proximities.
    """
    docs = retrieve_documents("compliance_docs", query, top_k)
    if not docs:
        return "No explicit compliance policies restricted limits."
    return "\n---\n".join([d["content"] for d in docs])
