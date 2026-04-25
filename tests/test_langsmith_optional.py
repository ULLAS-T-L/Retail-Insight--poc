import pytest
from src.observability.langsmith_tracer import langsmith_trace

@langsmith_trace("test_function")
def dummy_traced_function(x):
    if x < 0:
        raise ValueError("Negative number")
    return x * 2

def test_langsmith_optional_fallback_success():
    # Should execute normally without crashing, even if LangSmith is completely absent
    assert dummy_traced_function(5) == 10

def test_langsmith_optional_fallback_error():
    # Should still raise the native ValueError accurately without LangSmith interfering
    with pytest.raises(ValueError, match="Negative number"):
        dummy_traced_function(-1)
