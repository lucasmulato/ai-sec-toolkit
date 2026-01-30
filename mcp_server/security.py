import os
import functools
import time
import logging
import redis
from typing import Callable, Optional

# Setup Logging
logger = logging.getLogger("ARTT_Security")

# Redis Connection (Only connects if in Production)
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
except Exception as e:
    logger.warning(f"Redis not available, rate limiting disabled: {e}")
    redis_client = None

API_TOKEN = os.getenv("ARTT_MCP_TOKEN")

class SecurityMiddleware:
    
    @staticmethod
    def require_auth(func: Callable) -> Callable:
        """Enforces Token Authentication."""
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Check context/headers in real implementation
            # Here we check a simulated token kwarg or env var for CLI
            token = kwargs.get("token") or os.getenv("CLI_AUTH_TOKEN")
            
            if not API_TOKEN:
                logger.critical("Production Risk: ARTT_MCP_TOKEN is not set!")
                return {"error": "Configuration Error", "status": 500}

            if token != API_TOKEN:
                logger.warning(f"Unauthorized access attempt to {func.__name__}")
                return {"error": "Unauthorized: Invalid Access Token", "status": 403}
                
            return await func(*args, **kwargs)
        return wrapper

    @staticmethod
    def rate_limit(limit: int = 10, window: int = 60):
        """
        Redis-based Sliding Window Rate Limiter.
        Default: 10 requests per 60 seconds.
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                if not redis_client:
                    return await func(*args, **kwargs)

                # Use caller ID (IP or Token) as key. Simulating 'system' for now.
                caller_id = kwargs.get("user_id", "system_user")
                key = f"rate_limit:{caller_id}:{func.__name__}"
                
                current = redis_client.get(key)
                
                if current and int(current) >= limit:
                    logger.warning(f"Rate limit hit for {func.__name__} by {caller_id}")
                    return {"error": "Too Many Requests (Rate Limit Exceeded)", "status": 429}
                
                # Increment and expire
                pipe = redis_client.pipeline()
                pipe.incr(key)
                if not current:
                    pipe.expire(key, window)
                pipe.execute()
                
                return await func(*args, **kwargs)
            return wrapper
        return decorator

