"""
src/rag/cached_embedder.py

- Lazy-loads the sentence-transformers model on first use (not at import time)
  so startup is not blocked by the model download / GPU init.
- LRU-caches embedding vectors for repeated / identical queries so ChromaDB
  is not hit and the model is not re-run unnecessarily.
"""

from __future__ import annotations

import hashlib
import logging
import threading
from functools import lru_cache
from typing import List

logger = logging.getLogger(__name__)

_MODEL_NAME = "all-MiniLM-L6-v2"
_model = None
_lock = threading.Lock()


def _get_model():
    """Return the loaded SentenceTransformer model, loading it on first call."""
    global _model
    if _model is None:
        with _lock:
            if _model is None:          # double-checked locking
                logger.info("Loading sentence-transformers model: %s", _MODEL_NAME)
                from sentence_transformers import SentenceTransformer  # lazy import
                _model = SentenceTransformer(_MODEL_NAME)
                logger.info("Model loaded.")
    return _model


def _cache_key(text: str) -> str:
    """Stable cache key — normalize whitespace then hash."""
    normalized = " ".join(text.lower().split())
    return hashlib.sha256(normalized.encode()).hexdigest()


# LRU cache keyed on the normalized hash; 512 entries ≈ a few MB of float32 vectors.
@lru_cache(maxsize=512)
def _cached_encode(text_hash: str, text: str) -> tuple:
    """
    Inner cached function. text_hash is the cache key; text is the actual input.
    Returns a tuple so it is hashable and cacheable.
    """
    model = _get_model()
    vector = model.encode(text, normalize_embeddings=True)
    return tuple(vector.tolist())


def embed(text: str) -> List[float]:
    """
    Public API: embed a single string.
    Returns a list of floats (the embedding vector).
    Repeated calls with the same (or equivalent) text are served from cache.
    """
    key = _cache_key(text)
    return list(_cached_encode(key, text))


def embed_batch(texts: List[str]) -> List[List[float]]:
    """
    Embed a batch of strings.
    Each text is individually checked against the cache; only cache misses
    are forwarded to the model for encoding.
    """
    results: List[List[float] | None] = [None] * len(texts)
    miss_indices: List[int] = []
    miss_texts: List[str] = []

    for i, text in enumerate(texts):
        key = _cache_key(text)
        cached = _cached_encode.cache_info()  # for logging only
        try:
            results[i] = list(_cached_encode(key, text))
        except Exception:
            miss_indices.append(i)
            miss_texts.append(text)

    if miss_texts:
        logger.debug("Embedding %d cache misses in batch.", len(miss_texts))
        model = _get_model()
        vectors = model.encode(miss_texts, normalize_embeddings=True)
        for idx, vec in zip(miss_indices, vectors):
            results[idx] = vec.tolist()

    return results  # type: ignore[return-value]


def cache_info() -> dict:
    """Return LRU cache statistics for observability."""
    info = _cached_encode.cache_info()
    return {
        "hits": info.hits,
        "misses": info.misses,
        "maxsize": info.maxsize,
        "currsize": info.currsize,
    }
