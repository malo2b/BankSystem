from fastapi import APIRouter, Depends, status

from ..services.transaction_services import TransactionService
from ..schemas.pagination_schemas import Paginated
from ..schemas.transaction_schemas import TransactionRequest
from ..helpers.response import HTTPResponse

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/{account_id}")
async def get_transactions(
    account_id: int,
    paginated: Paginated = Depends(),
    service: TransactionService = Depends(),
):
    """Get transactions for a given account."""
    return HTTPResponse(
        status_code=status.HTTP_200_OK,
        content=await service.get_transactions(account_id, paginated),
    )


@router.post("/")
async def add_transaction(
    input: TransactionRequest,
    service: TransactionService = Depends(),
):
    """Get transactions for a given account."""
    return HTTPResponse(
        status_code=status.HTTP_201_CREATED,
        content=await service.add_transaction(input),
    )

__all__ = ["router"]
