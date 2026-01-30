import os
import functools
from typing import Callable

# Simple environment-based token check
API_TOKEN = os.getenv("ARTT_MCP_TOKEN", "default-insecure-token")

class SecurityMiddleware:
    @staticmethod
    def require_auth(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # In a real MCP request, you'd inspect the headers/context
            # For now, we simulate a check
            token = kwargs.get("token") 
            if token != API_TOKEN:
                return {"error": "Unauthorized: Invalid Access Token", "status": 403}
            return await func(*args, **kwargs)
        return wrapper

    @staticmethod
    def audit_log(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            print(f"[AUDIT] Tool '{func.__name__}' called with args: {args}")
            return await func(*args, **kwargs)
        return wrapper
