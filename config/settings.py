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
USE_LANGGRAPH = os.getenv("USE_LANGGRAPH", "True").lower() in ["true", "1"]
USE_RAG = os.getenv("USE_RAG", "True").lower() in ["true", "1"]
USE_EPISODIC_MEMORY = os.getenv("USE_EPISODIC_MEMORY", "True").lower() in ["true", "1"]
USE_SEMANTIC_MEMORY = os.getenv("USE_SEMANTIC_MEMORY", "True").lower() in ["true", "1"]
USE_GUARDRAILS = os.getenv("USE_GUARDRAILS", "True").lower() in ["true", "1"]
USE_OBSERVABILITY = os.getenv("USE_OBSERVABILITY", "True").lower() in ["true", "1"]

# Advanced Robustness Upgrade Flags (Part 3)
USE_ADVANCED_GUARDRAILS = os.getenv("USE_ADVANCED_GUARDRAILS", "True").lower() in ["true", "1"]
USE_TRULENS = os.getenv("USE_TRULENS", "False").lower() in ["true", "1"]
USE_LANGSMITH = os.getenv("USE_LANGSMITH", "False").lower() in ["true", "1"]

# RAG Configuration Parameters
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "3"))
RAG_MIN_SCORE = float(os.getenv("RAG_MIN_SCORE", "0.5"))

# Evaluation Paths
EVAL_RESULTS_DIR = os.getenv("EVAL_RESULTS_DIR", "evaluation_results")

# Enterprise Security Bounds (Part 4)
USE_AUTH = os.getenv("USE_AUTH", "True").lower() in ["true", "1"]
USE_RBAC = os.getenv("USE_RBAC", "True").lower() in ["true", "1"]
USE_API_KEY_FALLBACK = os.getenv("USE_API_KEY_FALLBACK", "True").lower() in ["true", "1"]

# JWT Core Configuration (Auto-generated fallback natively)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "b3d4f102581622f99a5e4d25725f49e41981a8c0879f82d1c67d7168d60d3d52")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "120"))

# Lightweight API Key check natively 
STATIC_API_KEY = os.getenv("STATIC_API_KEY", "secure-retail-key-123")
