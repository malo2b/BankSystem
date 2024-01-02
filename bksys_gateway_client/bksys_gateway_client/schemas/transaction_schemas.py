

from datetime import datetime
from enum import Enum

from pydantic import Field

from .pagination_schemas import Pagination
from .common_schemas import CamelCaseBaseModel


class TransactionType(str, Enum):
    """Transaction type."""
    INCOMING = "Incoming"
    OUTGOING = "Outgoing"


class Transaction(CamelCaseBaseModel):
    """Transaction."""
    id: int | None = Field()
    id_account: int = Field()
    amount: float = Field(ge=0)
    transaction_type: TransactionType = Field()
    transaction_date: datetime = Field()


class TransactionRequest(Transaction):
    """Transaction request."""
    id: int | None = None
    transaction_date: datetime = datetime.now()


class TransactionTransferRequest(CamelCaseBaseModel):
    """Transaction transfer request."""
    id_account_from: int = Field()
    id_account_to: int = Field()
    amount: float = Field(ge=0)


class PaginatedTransactionResponse(CamelCaseBaseModel):
    """Paginated transaction response."""
    data: list[Transaction]
    pagination: Pagination


__all__ = [
    "Transaction",
    "TransactionRequest",
    "TransactionTransferRequest",
    "TransactionType",
    "PaginatedTransactionResponse",
]
