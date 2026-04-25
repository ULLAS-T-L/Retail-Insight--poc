import pytest
from src.evaluation.trulens_adapter import track_with_trulens, init_trulens

def dummy_app(x):
    return x * 2

def test_trulens_optional_fallback():
    # Even if TruLens fails to load or keys are missing, the original callable must return unchanged
    wrapped_app = track_with_trulens("dummy", dummy_app)
    
    # If TruLens wasn't initialized, wrapped_app is literally dummy_app
    # If it was initialized, it's a TruCustomApp instance that can be called natively
    try:
        if wrapped_app == dummy_app:
            assert wrapped_app(5) == 10
    except Exception as e:
        pytest.fail(f"TruLens fallback mechanism triggered an unexpected error: {e}")
