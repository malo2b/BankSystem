"""TransactionService class."""

import logging
import aiohttp
from fastapi import Depends, HTTPException
from starlette import status
from circuitbreaker import circuit

from ..settings import app_settings
from ..schemas import (
    PaginatedTransactionResponse,
    Transaction,
    TransactionRequest,
    TransactionTransferRequest,
    TransactionType,
    Account,
    PaymentLimit,
    Paginated,
)
from ..services import OperationsRuleService, AccountService
from ..helpers.exceptions import ServerErrorException

log = logging.getLogger(__name__)


class TransactionService:
    """TransactionService class."""

    def __init__(
        self,
        account_service: AccountService = Depends(),
        operations_rule_service: OperationsRuleService = Depends(),
    ) -> None:
        """Init.

        Args:
            settings (AppSettings): App settings.
        """
        self.host: str = app_settings.TRANSACTION_MS_HOST
        self.account_service: AccountService = account_service
        self.operations_rule_service: OperationsRuleService = operations_rule_service

    async def health_check(self) -> bool:
        """Health check."""

        log.info(
            f"Requesting health check from transaction service. {self.host}/service-status"
        )
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.host}/service-status") as response:
                    return response.status == status.HTTP_200_OK
            except aiohttp.ClientError:
                log.error(
                    f"Error requesting health check from transaction service. {self.host}/service-status"
                )
                raise ServerErrorException(status_code=503, detail="Service Unavailable")

    @circuit(
        failure_threshold=app_settings.CIRCUIT_BREAKER_FAILURE_THRESHOLD,
        expected_exception=ServerErrorException,
        recovery_timeout=app_settings.CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    )
    async def get_transactions(self, account_id: str, paginated: Paginated) -> list:
        log.info(
            f"Requesting transactions from transaction service. {self.host}/transactions/{account_id}"
        )
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"{self.host}/transactions/{account_id}", params=paginated.model_dump(by_alias=True)
                ) as response:
                    if response.status == status.HTTP_404_NOT_FOUND:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail="Account not found",
                        )
                    result = await response.json()
                    return PaginatedTransactionResponse(**result)
            except aiohttp.ClientError:
                log.error(
                    f"Error requesting transactions from transaction service.\
                    {self.host}/transactions/{account_id}"
                )
                raise ServerErrorException(status_code=503, detail="Service Unavailable")

    @circuit(
        failure_threshold=app_settings.CIRCUIT_BREAKER_FAILURE_THRESHOLD,
        expected_exception=ServerErrorException,
        recovery_timeout=app_settings.CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    )
    async def _emit_transaction(self, transaction: Transaction) -> None:
        """Emit transaction.

        Args:
            transaction (Transaction): Transaction.

        Raises:
            HTTPException:
                - HTTP_400_BAD_REQUEST if transaction is not emitted
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.host}/transactions/",
                    data=transaction.model_dump_json(),
                    headers={"Content-Type": "application/json"},
                ) as response:
                    if response.status == status.HTTP_201_CREATED:
                        return
                    else:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error emitting transaction",
                        )

            except aiohttp.ClientError:
                log.error(
                    f"Error requesting transactions from transaction service.\
                    {self.host}/transactions/{transaction.id_account}"
                )
                raise ServerErrorException(status_code=503, detail="Service Unavailable")

    @circuit(
        failure_threshold=app_settings.CIRCUIT_BREAKER_FAILURE_THRESHOLD,
        expected_exception=ServerErrorException,
        recovery_timeout=app_settings.CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    )
    async def add_transaction(
        self,
        transaction: TransactionTransferRequest,
    ) -> None:
        """Check if account has enough money, has enough rights and emit transaction.

        Args:
            transaction (TransactionTransferRequest): Transaction transfer request.

        """
        log.info(
            f"Requesting transactions from transaction service. {self.host}/transactions"
        )
        # Check if account from and account to are different
        if transaction.id_account_from == transaction.id_account_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account from and account to must be different",
            )

        # Get account informations
        account_from: Account = (
            await self.account_service.get_account(transaction.id_account_from)
        ).data
        # Check account type
        if account_from.account_type == "Savings":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not authorized, account type not allowed",
            )
        # Check account balance
        if account_from.balance < transaction.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not authorized, account balance exceeded",
            )

        # Check account limit
        payment_limit: PaymentLimit = (
            await self.operations_rule_service.get_operations_rule_from_account(
                account_id=transaction.id_account_from
            )
        )
        if payment_limit.current_limit < transaction.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not authorized, payment limit exceeded",
            )

        # Emit transaction
        transaction: Transaction = TransactionRequest(
            id_account=transaction.id_account_from,
            amount=transaction.amount,
            transaction_type=TransactionType.OUTGOING,
        )
        # NOTE: here we should send transaction to a payment processor to pay the transaction
        # here we just emit the transaction internally
        await self._emit_transaction(transaction=transaction)


__all__ = ["TransactionService"]
