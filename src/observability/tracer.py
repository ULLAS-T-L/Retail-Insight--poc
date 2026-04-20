import time
import json
import logging
from typing import Callable, Any
from functools import wraps

# Establish root logger natively bounds securely JSON schema
logger = logging.getLogger("retail_insights_tracer")
logger.setLevel(logging.INFO)

# Provide simple stdout bounds
if not logger.handlers:
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

def emit_event(event_type: str, data: dict):
    payload = {
        "event": event_type,
        "timestamp": time.time(),
        **data
    }
    logger.info(json.dumps(payload))

def trace_event(event_name: str) -> Callable:
    """Decorator capturing performance metrics correctly effortlessly natively seamlessly."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            error = None
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                error = str(e)
                raise
            finally:
                latency = time.time() - start_time
                emit_event(event_name, {
                    "latency_sec": round(latency, 4),
                    "success": error is None,
                    "error": error
                })
        return wrapper
    return decorator
