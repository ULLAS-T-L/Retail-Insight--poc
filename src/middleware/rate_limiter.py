"""
src/middleware/rate_limiter.py

Per-IP rate limiting for the /analyze endpoint using slowapi (a Starlette/FastAPI
wrapper around limits).

Integration — in src/main.py:
    from src.middleware.rate_limiter import limiter, rate_limit_exceeded_handler
    from slowapi.errors import RateLimitExceeded

    app = FastAPI(lifespan=lifespan)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

Then decorate any route:
    @router.post("/analyze")
    @limiter.limit("20/minute")
    async def analyze(request: Request, ...):
        ...
"""

from __future__ import annotations

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200/hour"],       # global default for all routes
)

# Per-endpoint overrides (apply as decorator arguments):
ANALYZE_LIMIT = "20/minute"           # LLM calls are expensive
AUTH_LIMIT = "10/minute"              # brute-force protection on login


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """Return a clean 429 JSON response instead of the default text error."""
    return JSONResponse(
        status_code=429,
        content={
            "error": "rate_limit_exceeded",
            "detail": f"Too many requests. Limit: {exc.detail}",
        },
        headers={"Retry-After": "60"},
    )
