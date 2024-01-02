"""Accounts schemas."""

from enum import Enum
from pydantic import Field
from .common_schemas import CamelCaseBaseModel
from .pagination_schemas import Pagination


class AccountType(str, Enum):
    """Account type."""

    CURRENT = "Current"
    SAVINGS = "Savings"


class Account(CamelCaseBaseModel):
    """Account schema."""

    account_id: int = Field()
    user_id: int = Field()
    account_type: AccountType = Field()
    account_number: int = Field()
    balance: float = Field()


class AccountResponse(CamelCaseBaseModel):
    """Account response schema."""

    data: Account


class PaginatedAccountResponse(CamelCaseBaseModel):
    """Paginated account response schema."""

    data: list[Account]
    pagination: Pagination


__all__ = [
    "Account",
    "AccountResponse",
    "PaginatedAccountResponse",
    "AccountType",
]
