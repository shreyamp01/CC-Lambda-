from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time, logging

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        logging.info(f"{request.url.path} - {request.method} - {duration:.2f}s")
        return response
