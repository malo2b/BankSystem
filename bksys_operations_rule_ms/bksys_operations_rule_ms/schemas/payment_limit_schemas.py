
from pydantic import Field
from .common_schemas import CamelCaseBaseModel


class PaymentLimit(CamelCaseBaseModel):
    """Payment limit schema."""
    user_id: int = Field()
    account_id: int = Field()
    current_limit: float = Field()


__all__ = ["PaymentLimit"]
