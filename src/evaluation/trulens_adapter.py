import os
import logging
from config.settings import USE_TRULENS, get_gemini_key

logger = logging.getLogger(__name__)

# Attempt to load TruLens natively safely
try:
    if USE_TRULENS:
        from trulens_eval import Tru, Feedback
        from trulens_eval.feedback.provider.litellm import LiteLLM
        HAS_TRULENS = True
    else:
        HAS_TRULENS = False
except ImportError:
    HAS_TRULENS = False
    if USE_TRULENS:
        logger.warning("TruLens is effectively requested but not installed. Skipping TruLens bindings smoothly.")

def init_trulens():
    if not HAS_TRULENS:
        return None, None
        
    try:
        tru = Tru()
        
        # Setting up LiteLLM Provider using Gemini (requires `gemini/` prefix for liteLLM)
        gemini_key = get_gemini_key()
        os.environ["GEMINI_API_KEY"] = gemini_key
        provider = LiteLLM(model_engine="gemini/gemini-2.5-flash")
        
        # Triad definitions
        f_groundedness = Feedback(provider.groundedness_measure_with_cot_reasons).on(
            getattr(Tru(), "record").app.context
        ).on(
            getattr(Tru(), "record").main_output
        )
        
        f_answer_relevance = Feedback(provider.relevance_with_cot_reasons).on_input_output()
        f_context_relevance = Feedback(provider.context_relevance_with_cot_reasons).on_input().on(
            getattr(Tru(), "record").app.context
        )
        
        feedbacks = [f_groundedness, f_answer_relevance, f_context_relevance]
        return tru, feedbacks
    except Exception as e:
        logger.error(f"TruLens initialization failed: {e}. Falling back cleanly to local native metrics smoothly.")
        return None, None

def track_with_trulens(app_id: str, app_callable, **kwargs):
    """
    Wraps an application entrypoint intuitively safely.
    If TruLens is missing, completely skips cleanly.
    """
    tru, feedbacks = init_trulens()
    
    if tru and feedbacks:
        try:
            from trulens_eval import TruCustomApp
            tru_app = TruCustomApp(app_callable, app_id=app_id, feedbacks=feedbacks)
            return tru_app
        except Exception:
            pass
            
    # Fallback: Just return the original callable untouched
    return app_callable
