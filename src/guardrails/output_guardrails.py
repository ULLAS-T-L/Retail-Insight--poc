from typing import Dict, Any

class OutputGuardrailException(Exception):
    pass

def validate_response_structure(response: Dict[str, Any]) -> bool:
    """Ensures response has the required sections: summary, drivers, risks, actions"""
    required_keys = ["summary", "drivers", "actions"]
    for key in required_keys:
        if key not in response:
            raise OutputGuardrailException(f"Output is missing required key: '{key}'")
            
        if key in ["drivers", "actions"]:
            if not isinstance(response[key], list):
                 raise OutputGuardrailException(f"Output key '{key}' must be a list of strings.")
                 
    if "risks" in response and response["risks"] is not None:
        if not isinstance(response["risks"], list):
            raise OutputGuardrailException("Output key 'risks' must be a list of strings if provided.")
            
    return True
