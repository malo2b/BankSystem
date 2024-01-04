"""AccountService class."""

import logging
import aiohttp
from fastapi import HTTPException
from starlette import status
from circuitbreaker import circuit

from ..settings import app_settings
from ..schemas import AccountResponse, PaginatedAccountResponse, Paginated
from ..helpers.exceptions import ServerErrorException

log = logging.getLogger(__name__)


class AccountService:
    """AccountService class."""

    def __init__(self) -> None:
        """Init.

        Args:
            settings (AppSettings): App settings.
        """
        self.host: str = app_settings.ACCOUNT_MS_HOST

    @circuit(
        failure_threshold=app_settings.CIRCUIT_BREAKER_FAILURE_THRESHOLD,
        expected_exception=ServerErrorException,
        recovery_timeout=app_settings.CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    )
    async def health_check(self) -> bool:
        """Health check."""

        log.info(
            f"Requesting health check from account service. {self.host}/service-status"
        )
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.host}/service-status") as response:
                    return response.status == 200
            except aiohttp.ClientError:
                log.error(f"Error requesting health check from account service. {self.host}/service-status")
                raise ServerErrorException(status_code=503, detail="Service Unavailable")

    @circuit(
        failure_threshold=app_settings.CIRCUIT_BREAKER_FAILURE_THRESHOLD,
        expected_exception=ServerErrorException,
        recovery_timeout=app_settings.CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    )
    async def get_accounts(self, paginated: Paginated) -> PaginatedAccountResponse:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"{self.host}/accounts", params=paginated.model_dump(by_alias=True)
                ) as response:
                    if response.status == status.HTTP_404_NOT_FOUND:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail="Accounts not found",
                        )
                    result = await response.json()
                    return PaginatedAccountResponse(**result)
            except aiohttp.ClientError:
                log.error(f"Error requesting accounts from account service. {self.host}/accounts")
                raise ServerErrorException(status_code=503, detail="Service Unavailable")

    @circuit(
        failure_threshold=app_settings.CIRCUIT_BREAKER_FAILURE_THRESHOLD,
        expected_exception=ServerErrorException,
        recovery_timeout=app_settings.CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    )
    async def get_account(self, account_id: str) -> AccountResponse:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"{self.host}/accounts/{account_id}"
                ) as response:
                    if response.status == status.HTTP_404_NOT_FOUND:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail="Account not found",
                        )
                    result = await response.json()
                    return AccountResponse(**result)
            except aiohttp.ClientError:
                log.error(f"Error requesting account from account service. {self.host}/accounts/{account_id}")
                raise ServerErrorException(status_code=503, detail="Service Unavailable")


__all__ = ["AccountService"]
