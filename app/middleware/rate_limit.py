from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import get_settings

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.settings = get_settings()
        self._requests: dict = defaultdict(list)