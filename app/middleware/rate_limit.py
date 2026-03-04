from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from app.config.redis_client import get_redis_client
from app.core.response import error_response
from app.core.error_codes import ERROR_CODES
from app.core.logger import logger
from app.config.bootstrap_settings import bootstrap_settings
from app.config.config_manager import get_settings
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request, call_next):
        

        settings = get_settings()

        redis_client = get_redis_client()
        
        max_req = int(settings.RATE_LIMIT_MAX or 100)
        window = int(settings.RATE_LIMIT_WINDOW or 60)
        key = f"rate:{request.client.host}:{int(time.time()) // window}"
        print ("max request is ", max_req)
        print ("windows is", window)
        count = redis_client.incr(key)
        if count == 1:
            redis_client.expire(key, window)
        if count > max_req:
            return JSONResponse(status_code=429,
                content=error_response("RATE_001", ERROR_CODES["RATE_001"], "N/A"))
        return await call_next(request)