from fastapi import Security, HTTPException, status, Request
from fastapi.security import APIKeyHeader
from src.config import settings
import time
from collections import defaultdict

# Setup Header Extraction for "X-API-Key"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return api_key

# In-Memory Sliding Window Rate Limiter 
class RateLimiter:
    def __init__(self, limit: int, window_seconds: int = 60):
        self.limit = limit
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        # Clean up old footprints
        self.requests[client_id] = [t for t in self.requests[client_id] if now - t < self.window_seconds]
        
        if len(self.requests[client_id]) >= self.limit:
            return False
        
        self.requests[client_id].append(now)
        return True

limiter = RateLimiter(limit=settings.RATE_LIMIT_PER_MIN)

def check_rate_limit(request: Request):
    """ Dependency to limit API calls per minute based on IP """
    client_ip = request.client.host if request.client else "unknown"
    if not limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
