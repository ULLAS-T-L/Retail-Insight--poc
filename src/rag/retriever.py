from typing import List, Dict, Any
from src.rag.indexer import get_chroma_client

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
            for doc in results["documents"][0]:
                documents.append({"content": doc})
        return documents
    except Exception as e:
        print(f"Retrieval gracefully bypassed missing index limitations: {str(e)}")
        return []
