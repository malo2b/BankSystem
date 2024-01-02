from fastapi import APIRouter, Depends, status

from ..helpers.response import HTTPResponse
from ..services.payment_limit_services import PaymentLimitService

router = APIRouter(prefix="/payment-limits", tags=["payment-limits"])


@router.get("/users/{user_id}")
async def get_payment_limit(user_id: int, service: PaymentLimitService = Depends()):
    """Get payment limit for user."""
    return HTTPResponse(
        status_code=status.HTTP_200_OK, content=await service.get_payment_limit(user_id)
    )


@router.get("/accounts/{account_id}")
async def get_payment_limit_by_account(
    account_id: int, service: PaymentLimitService = Depends()
):
    """Get payment limit for account."""
    return HTTPResponse(
        status_code=status.HTTP_200_OK,
        content=await service.get_payment_limit_by_account(account_id),
    )
