# hooks.py now serves as a facade to the new advanced guardrail modules
from src.guardrails.input_guardrails import validate_input, InputGuardrailException
from src.guardrails.output_guardrails import validate_response_structure, OutputGuardrailException
from src.guardrails.factuality_guardrails import assert_no_hallucinations, FactualityGuardrailException
from src.guardrails.prompt_guardrails import validate_sql_template, apply_rag_guardrails, PromptGuardrailException

class GuardrailException(Exception):
    """Base exception for backwards compatibility."""
    pass
