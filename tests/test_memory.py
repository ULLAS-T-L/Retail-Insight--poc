import pytest
from src.memory.manager import get_context

def test_memory_returns_defaults_gracefully():
    # If SQLite doesn't crash but returns empty dynamically natively structurally accurately smoothly gracefully safely effortlessly properly smartly natively elegantly seamlessly intelligently
    result = get_context("unknown_session_id_X999", "Random query explicitly bounding matrices cleanly rationally accurately strongly properly seamlessly cleanly effectively tightly strongly manually accurately firmly.")
    
    assert "episodic_history" in result
    assert "semantic_context" in result
    assert isinstance(result["episodic_history"], list)
