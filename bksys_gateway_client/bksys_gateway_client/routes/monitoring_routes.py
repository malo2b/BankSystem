"""Monitoring routes."""

import asyncio
import logging
from fastapi import APIRouter, Depends, Response
from starlette import status

from ..services.operations_rule_service import OperationsRuleService
from ..services.accounts_service import AccountService
from ..services.transaction_service import TransactionService

log = logging.getLogger(__name__)

router = APIRouter()


@router.get("/service-status", tags=["monitoring"])
async def service_status():
    """Return service status."""
    log.info("Service status requested.")
    return Response(status_code=status.HTTP_200_OK, content="Service OK")


@router.get("/dependencies-status", tags=["monitoring"])
async def dependencies_status(
    operations_rule_service: OperationsRuleService = Depends(),
    account_service: AccountService = Depends(),
    transaction_service: TransactionService = Depends(),
):
    """Return dependencies status."""

    log.info("Dependencies status requested.")

    await asyncio.gather(
            operations_rule_service.health_check(),
            account_service.health_check(),
            transaction_service.health_check(),
        )

    return Response(status_code=status.HTTP_200_OK, content="Dependencies OK")


__all__ = ["router"]
