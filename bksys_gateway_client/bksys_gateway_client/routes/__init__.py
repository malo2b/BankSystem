"""Routes module."""

from fastapi import APIRouter

from .accounts_routes import router as accounts_router
from .operations_rule_routes import router as operations_rule_router
from .transactions_routes import router as transactions_router
from .monitoring_routes import router as monitoring_router

router = APIRouter()
router.include_router(monitoring_router)
router.include_router(transactions_router)
router.include_router(accounts_router)
router.include_router(operations_rule_router)

__all__ = ["router"]
