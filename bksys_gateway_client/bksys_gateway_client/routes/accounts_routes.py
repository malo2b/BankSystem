

from fastapi import APIRouter, Depends, status

from ..helpers.response import HTTPResponse
from ..schemas import Paginated
from ..services.accounts_service import AccountService


router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/")
async def get_accounts(service: AccountService = Depends(), paginated: Paginated = Depends()):
    """Get accounts."""
    return HTTPResponse(
        status_code=status.HTTP_200_OK,
        content=await service.get_accounts(paginated),
    )


@router.get("/{account_id}")
async def get_account(account_id: int, service: AccountService = Depends()):
    """Get account."""
    return HTTPResponse(
        status_code=status.HTTP_200_OK,
        content=await service.get_account(account_id=account_id),
    )
