from typing import List, Dict, Any
from src.rag.indexer import get_chroma_client
from chromadb.utils import embedding_functions

def get_semantic_collection():
    client = get_chroma_client()
    default_ef = embedding_functions.DefaultEmbeddingFunction()
    return client.get_or_create_collection(
        name="semantic_memory",
        embedding_function=default_ef
    )

def store_embedding(session_id: str, context: str, metadata: Dict[str, Any]) -> None:
    """
    Indefinitely stores generalized insights extracting deep personalized mapping paths natively.
    """
    try:
        collection = get_semantic_collection()
        doc_id = f"{session_id}_{hash(context)}"
        
        # Inject standard bindings securely inside memory keys
        meta = metadata.copy()
        meta["session_id"] = session_id
        
        collection.upsert(
            documents=[context],
            metadatas=[meta],
            ids=[doc_id]
        )
    except Exception as e:
        print(f"Failed to embed semantic memory limit gracefully: {e}")

def retrieve_similar_context(session_id: str, query: str, top_k: int = 3) -> str:
    """
    Queries past conceptual boundaries uniquely matching active semantic vector traits tightly.
    """
    try:
        collection = get_semantic_collection()
        results = collection.query(
            query_texts=[query],
            n_results=top_k,
            where={"session_id": session_id}
        )
        
        texts = []
        if results and "documents" in results and results["documents"] and results["documents"][0]:
            texts = results["documents"][0]
        return "\n".join(texts)
    except Exception:
        return ""
