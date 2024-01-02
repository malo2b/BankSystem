"""Initialize client gateway."""

import logging
from multiprocessing import Queue

from circuitbreaker import CircuitBreakerError
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from logging_loki import LokiQueueHandler
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.requests import Request as StarletteRequest

from .helpers import HTTPResponse, EndpointFilter
from .routes import router
from .settings import app_settings
from .schemas import CircuitBreakerResponse


logging.basicConfig(format='%(levelname)s : %(asctime)s : [%(name)s]: %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


# Initialize FastAPI app
app = FastAPI()
log.info("Initializing FastAPI app.")


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(CircuitBreakerError)
async def circuit_breaker_error_handler(request: StarletteRequest, exc: CircuitBreakerError) -> None:
    """Circuit breaker error handler."""
    return HTTPResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=CircuitBreakerResponse(
            message="Circuit breaker error",
            open_until=str(exc._circuit_breaker.open_until),
            failure_count=exc._circuit_breaker.failure_count,
            failure_threshold=app_settings.CIRCUIT_BREAKER_FAILURE_THRESHOLD,
            detail=str(exc)
        ),
    )


# Import routes
app.include_router(router)
# Prometheus metrics
Instrumentator().instrument(app).expose(app, tags=["monitoring"])

# Loki logging
loki_logs_handler = LokiQueueHandler(
    Queue(-1),
    url=app_settings.LOKI_ENDPOINT,
    tags={"application": "fastapi", "service": "bksys_gateway_client"},
    version="1",
)

uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.addHandler(loki_logs_handler)

# Filter out health check endpoint from access logs
uvicorn_access_logger.addFilter(EndpointFilter("/service-status"))
uvicorn_access_logger.addFilter(EndpointFilter("/metrics"))


__all__ = ["app"]
