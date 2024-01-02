from fastapi import APIRouter

from .monitoring import router as monitoring_router
from .payment_limit_routes import router as payment_limit_router

router = APIRouter()
router.include_router(monitoring_router)
router.include_router(payment_limit_router)

__all__ = ["router"]
