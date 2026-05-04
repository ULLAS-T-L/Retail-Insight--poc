"""
src/cache/response_cache.py

Lightweight in-memory TTL cache for KPI query responses.
Common retail KPIs (daily sales, top SKUs, inventory levels) change infrequently,
so caching for a short window (default 120 s) avoids redundant LLM + DB calls.

Usage:
    from src.cache.response_cache import get_cached, set_cached, invalidate

    cached = get_cached(query)
    if cached:
        return cached

    result = await expensive_analyze(query)
    set_cached(query, result)
    return result
"""

from __future__ import annotations

import hashlib
import logging
import time
from threading import Lock
from typing import Any

logger = logging.getLogger(__name__)

_DEFAULT_TTL = 120  # seconds

_store: dict[str, tuple[Any, float]] = {}   # key → (value, expiry_timestamp)
_lock = Lock()


def _make_key(query: str) -> str:
    """Normalize the query and return a stable cache key."""
    normalized = " ".join(query.lower().split())
    return hashlib.sha256(normalized.encode()).hexdigest()


def get_cached(query: str) -> Any | None:
    """
    Return the cached response for this query, or None if not found / expired.
    Expired entries are evicted on access.
    """
    key = _make_key(query)
    with _lock:
        entry = _store.get(key)
        if entry is None:
            return None
        value, expiry = entry
        if time.monotonic() > expiry:
            del _store[key]
            logger.debug("Cache expired for key %s…", key[:8])
            return None
        logger.debug("Cache hit for key %s…", key[:8])
        return value


def set_cached(query: str, value: Any, ttl: int = _DEFAULT_TTL) -> None:
    """Store a response in the cache with a TTL in seconds."""
    key = _make_key(query)
    expiry = time.monotonic() + ttl
    with _lock:
        _store[key] = (value, expiry)
    logger.debug("Cached response for key %s… (TTL=%ds)", key[:8], ttl)


def invalidate(query: str) -> bool:
    """Explicitly remove a single entry. Returns True if it existed."""
    key = _make_key(query)
    with _lock:
        existed = key in _store
        _store.pop(key, None)
    return existed


def clear_all() -> int:
    """Flush the entire cache. Returns the number of entries removed."""
    with _lock:
        count = len(_store)
        _store.clear()
    logger.info("Cache flushed (%d entries removed).", count)
    return count


def stats() -> dict:
    """Return current cache stats for the /health or observability endpoint."""
    now = time.monotonic()
    with _lock:
        total = len(_store)
        expired = sum(1 for _, (_, exp) in _store.items() if now > exp)
    return {"total_entries": total, "expired_pending_eviction": expired}
