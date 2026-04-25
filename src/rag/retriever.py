from typing import List, Dict, Any
from src.rag.indexer import get_chroma_client

from src.observability.langsmith_tracer import langsmith_trace

@langsmith_trace("rag_retrieval")
def retrieve_documents(collection_name: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Generic ChromaDB fetch interface smoothly bouncing bounds natively ignoring crash logic.
    """
    try:
        from chromadb.utils import embedding_functions
        client = get_chroma_client()
        default_ef = embedding_functions.DefaultEmbeddingFunction()
        collection = client.get_collection(name=collection_name, embedding_function=default_ef)
        
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        documents = []
        if results and "documents" in results and results["documents"] and results["documents"][0]:
            docs = results["documents"][0]
            metas = results["metadatas"][0] if "metadatas" in results and results["metadatas"] else [{}] * len(docs)
            distances = results["distances"][0] if "distances" in results and results["distances"] else [0.0] * len(docs)
            
            for doc, meta, dist in zip(docs, metas, distances):
                documents.append({
                    "content": doc,
                    "metadata": meta,
                    "distance": dist
                })
        return documents
    except Exception as e:
        print(f"Retrieval gracefully bypassed missing index limitations: {str(e)}")
        return []
