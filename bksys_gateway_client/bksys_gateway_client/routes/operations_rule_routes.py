

from fastapi import APIRouter, Depends, status

from ..helpers.response import HTTPResponse

from ..services.operations_rule_service import OperationsRuleService


router = APIRouter(prefix="/operations-rule", tags=["operations-rule"])


@router.get("/accounts/{account_id}")
async def get_operations_rule_from_account(account_id: int, service: OperationsRuleService = Depends()):
    """Get operations rule."""
    return HTTPResponse(
        status_code=status.HTTP_200_OK,
        content=await service.get_operations_rule_from_account(account_id=account_id),
    )


@router.get("/users/{user_id}")
async def get_operations_rule_from_user(user_id: int, service: OperationsRuleService = Depends()):
    """Get operations rule."""
    return HTTPResponse(
        status_code=status.HTTP_200_OK,
        content=await service.get_operations_rule_from_user(user_id=user_id),
    )
