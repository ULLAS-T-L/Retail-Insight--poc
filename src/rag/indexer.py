import os
import chromadb
from chromadb.utils import embedding_functions
from config.settings import CHROMA_DB_PATH

def get_chroma_client():
    # Utilizing Chroma Persistent storage without local Dockers natively
    return chromadb.PersistentClient(path=CHROMA_DB_PATH)

def get_compliance_collection():
    client = get_chroma_client()
    default_ef = embedding_functions.DefaultEmbeddingFunction()
    return client.get_or_create_collection(
        name="compliance_docs",
        embedding_function=default_ef
    )

def index_documents(docs_dir: str = "data/compliance_docs/") -> bool:
    """
    RAG ingestion pipeline. Scans local explicit markdown bounds and indexes symmetrically.
    """
    if not os.path.exists(docs_dir):
        return False
        
    collection = get_compliance_collection()
    
    docs = []
    ids = []
    
    for filename in os.listdir(docs_dir):
        if filename.endswith(".md") or filename.endswith(".txt"):
            filepath = os.path.join(docs_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extremely primitive dense chunking specifically for POC contexts natively
                chunks = [chunk for chunk in content.split("\n\n") if len(chunk.strip()) > 20]
                for i, chunk in enumerate(chunks):
                    docs.append(chunk.strip())
                    ids.append(f"{filename}_chunk_{i}")

    if docs:
        collection.upsert(
            documents=docs,
            ids=ids
        )
    return True
