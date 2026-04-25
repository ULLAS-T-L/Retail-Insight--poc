import os
import time
from functools import wraps
from typing import Callable, Any
from config.settings import USE_LANGSMITH

# Import the existing local tracker for fallback
from src.observability.tracer import emit_event

# Attempt to import langsmith securely
try:
    from langsmith import Client, RunTree
    HAS_LANGSMITH = True
except ImportError:
    HAS_LANGSMITH = False

def langsmith_trace(name: str) -> Callable:
    """
    Optional LangSmith decorator.
    If LangSmith is configured correctly it logs spans to the LangChain dashboard.
    If disabled or missing, perfectly falls back to our local robust emit_event.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            
            # Check explicit bounds logically
            use_smith = (
                USE_LANGSMITH and 
                HAS_LANGSMITH and 
                os.getenv("LANGCHAIN_API_KEY") and 
                os.getenv("LANGCHAIN_TRACING_V2", "").lower() == "true"
            )
            
            start_time = time.time()
            error = None
            
            if use_smith:
                try:
                    # Dynamically construct the span correctly reliably flexibly
                    rt = RunTree(
                        name=name,
                        run_type="chain",
                        inputs={"args": args, "kwargs": kwargs}
                    )
                    rt.post()
                    
                    try:
                        result = func(*args, **kwargs)
                        rt.end(outputs={"result": result})
                        rt.patch()
                        return result
                    except Exception as inner_e:
                        rt.end(error=str(inner_e))
                        rt.patch()
                        raise
                        
                except Exception as eval_e:
                    # If LangSmith crashes, gracefully silently fallback logically
                    error = str(eval_e)
                    pass
            
            # Pure local fallback mechanism natively
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                error = str(e)
                raise
            finally:
                latency = time.time() - start_time
                emit_event(f"local_fallback_{name}", {
                    "latency_sec": round(latency, 4),
                    "success": error is None,
                    "error": error
                })
                
        return wrapper
    return decorator
