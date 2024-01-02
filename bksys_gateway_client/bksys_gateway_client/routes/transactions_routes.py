"""Transactions routes."""

import logging
from fastapi import APIRouter, Depends, status, Response

from ..helpers.response import HTTPResponse
from ..services.transaction_service import TransactionService
from ..schemas import TransactionTransferRequest

log = logging.getLogger(__name__)


router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/{account_id}")
async def get_transactions(account_id: str, service: TransactionService = Depends()):
    """Get transactions."""
    return HTTPResponse(
        status_code=status.HTTP_200_OK,
        content=await service.get_transactions(account_id=account_id),
    )


@router.post("/{account_id}")
async def add_transaction(
    transaction: TransactionTransferRequest,
    service: TransactionService = Depends(),
):
    """Transfer."""
    await service.add_transaction(transaction)
    return Response(status_code=status.HTTP_201_CREATED)
