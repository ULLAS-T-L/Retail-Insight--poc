import re

class InputGuardrailException(Exception):
    pass

def sanitize_sql(query: str) -> str:
    """Removes destructive SQL clauses."""
    unsafe_patterns = [r"drop\s+table", r"delete\s+from", r"update\s+", r"insert\s+into", r";"]
    sanitized = query
    for pattern in unsafe_patterns:
        sanitized = re.sub(pattern, "", sanitized, flags=re.IGNORECASE)
    return sanitized.strip()

def block_prompt_injection(query: str) -> str:
    """Blocks common prompt injection techniques."""
    injection_phrases = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "reveal system prompt",
        "write sql directly",
        "generate arbitrary sql",
        "forget your instructions"
    ]
    lower_query = query.lower()
    for phrase in injection_phrases:
        if phrase in lower_query:
            raise InputGuardrailException(f"Prompt injection attempt detected: '{phrase}'. Request blocked.")
    return query

def validate_input(query: str) -> str:
    """
    Validates explicit query bounds, rejects empty strings, bounds length,
    and sanitizes against SQL/Prompt Injection attacks.
    """
    if not query or not query.strip():
        raise InputGuardrailException("Input query cannot be empty.")
        
    if len(query) > 500:
        raise InputGuardrailException("Input query exceeds the 500 character limit.")
        
    query = block_prompt_injection(query)
    query = sanitize_sql(query)
    
    return query
