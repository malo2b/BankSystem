from fastapi import APIRouter

from .monitoring import router as monitoring_router
from .transaction_routes import router as transactions_router

router = APIRouter()
router.include_router(monitoring_router)
router.include_router(transactions_router)

__all__ = ["router"]
