from typing import Dict, Any, Tuple
from config.settings import RAG_MIN_SCORE

class PromptGuardrailException(Exception):
    pass

def validate_sql_template(sql_template: str, allowed_templates: list) -> bool:
    """Ensures only permitted SQL templates are used."""
    if sql_template not in allowed_templates:
        raise PromptGuardrailException(f"SQL Template '{sql_template}' is not in the allowed templates list.")
    return True

def apply_rag_guardrails(documents: list, scores: list) -> Tuple[str, bool]:
    """
    Checks if retrieved context meets RAG_MIN_SCORE.
    If yes, returns the combined context.
    If no, returns empty string and sets a flag that context is insufficient.
    """
    if not documents or not scores:
        return "", False
        
    filtered_docs = []
    # Lower distance in Chroma means a higher score in cosine similarity for distance algorithms
    # Assuming the local implementation passes distances as "scores"
    for doc, dist in zip(documents, scores):
        # We will assume a lower distance denotes higher relevancy
        # In typical chroma setups, distance < RAG_MIN_SCORE means it is relevant
        # If your local structure uses cosine similarity instead of L2 distance, then dist > RAG_MIN_SCORE might be needed.
        # We assume smaller distance is better for ChromaDB L2 defaults.
        if float(dist) <= float(RAG_MIN_SCORE):
            filtered_docs.append(doc)
            
    if not filtered_docs:
        return "", False # Insufficient context
        
    return "\n\n".join(filtered_docs), True
