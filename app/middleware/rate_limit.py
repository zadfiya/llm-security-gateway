from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import get_settings
from starlette.requests import Request
from starlette.responses import JSONResponse

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.settings = get_settings()
        self._requests: dict = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        now = time.time()
        window = self.settings.rate_limit_window
        limit = self.settings.rate_limit_requests

        # Remove timestamps outside current window
        self._requests[ip] = [t for t in self._requests[ip] if now - t < window]

        if len(self._requests[ip]) >= limit:
            return JSONResponse(
                status_code=429,
                content={"Error_Code": "RATE_LIMIT_EXCEEDED",
                "Error_Message":"Too Many Requests", 
                "detail": "Rate limit exceeded. Try again later."}
            ):

        self._requests[ip].append(now)
        return await call_next(request)