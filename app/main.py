from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.config.config_manager import config_manager
from app.core.exceptions import http_exception_handler
from app.core.logger import setup_logging
from app.core.response_middleware import StandardResponseMiddleware
from app.core.validation_handler import validation_exception_handler
from app.middleware.audit import AuditMiddleware
from app.middleware.auth import AuthMiddleware
from app.middleware.correlation_middleware import CorrelationIdMiddleware
from app.router.sample_router import router as sample_router
from app.router.user_router import router as user_router

setup_logging()
print("App starting")


@asynccontextmanager
async def lifespan(app: FastAPI):
    #  Load config BEFORE serving requests
    await config_manager.load_config()

    # Start listener
    listener_task = asyncio.create_task(
        config_manager.start_listener(),
    )

    yield

    listener_task.cancel()


app = FastAPI(title="AWS Enterprise FastAPI Starter", lifespan=lifespan)


# app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
# app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
# app.add_middleware(EncryptionMiddleware)
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(AuthMiddleware)
# app.add_middleware(RateLimitMiddleware)
app.add_middleware(AuditMiddleware)
app.add_middleware(StandardResponseMiddleware)
app.include_router(sample_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "success", "data": {"message": "OK"}}
