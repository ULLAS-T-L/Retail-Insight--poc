import os
from dotenv import load_dotenv

# Safely load variables from the .env file natively
load_dotenv()

# SQLite Pathing limits
DB_PATH = os.getenv("DB_PATH", "retail_data.db")
if DB_PATH.startswith("sqlite:///"):
    DB_PATH = DB_PATH.replace("sqlite:///", "")
    
# Local Persistent Memory Bounding
MEMORY_DB_PATH = os.getenv("MEMORY_DB_PATH", "memory.db")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", ".chroma_db/")

def get_gemini_key() -> str:
    """Extracts the Gemini API Key natively or raises a predictable failure."""
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY is missing from environment variables.")
    return key

# Part 2 Architecture Flags
USE_LANGGRAPH = True
USE_RAG = True
USE_EPISODIC_MEMORY = True
USE_SEMANTIC_MEMORY = True
USE_GUARDRAILS = False
USE_OBSERVABILITY = False
