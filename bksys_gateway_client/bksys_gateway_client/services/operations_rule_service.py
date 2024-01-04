"""OperationsRuleService class."""

import logging
import aiohttp
from fastapi import HTTPException
from starlette import status
from circuitbreaker import circuit

from ..settings import app_settings
from ..schemas.payment_limit_schemas import PaymentLimit

log = logging.getLogger(__name__)


class OperationsRuleService:
    """OperationsRuleService class."""

    def __init__(self) -> None:
        """Init.

        Args:
            settings (AppSettings): App settings.
        """
        self.host: str = app_settings.OPERATIONS_RULE_MS_HOST

    async def health_check(self) -> bool:
        """Health check.

        Raises:
            HTTPException:
             - HTTP_503_SERVICE_UNAVAILABLE if service is not available

        Returns:
            bool: True if service is available
        """

        log.info(
            f"Requesting health check from operations rule service. {self.host}/service-status"
        )
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.host}/service-status") as response:
                    return response.status == 200
            except aiohttp.ClientError:
                log.error(
                    f"Error requesting health check from operations rule service. {self.host}/service-status"
                )
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    @circuit(
        failure_threshold=app_settings.CIRCUIT_BREAKER_FAILURE_THRESHOLD,
        expected_exception=HTTPException,
        recovery_timeout=app_settings.CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    )
    async def get_operations_rule_from_account(self, account_id: int) -> PaymentLimit:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"{self.host}/payment-limits/accounts/{account_id}"
                ) as response:
                    if response.status == 404:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Payment limit not found for account {account_id}",
                        )
                    result = await response.json()
                    return PaymentLimit(**result)
            except aiohttp.ClientError:
                log.error(
                    f"Error requesting operations rule from operations rule service. \
                    {self.host}/payment-limit/{account_id}"
                )
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    @circuit(
        failure_threshold=app_settings.CIRCUIT_BREAKER_FAILURE_THRESHOLD,
        expected_exception=HTTPException,
        recovery_timeout=app_settings.CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    )
    async def get_operations_rule_from_user(self, user_id: int) -> PaymentLimit:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"{self.host}/payment-limits/users/{user_id}"
                ) as response:
                    if response.status == 404:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Payment limit not found for user {user_id}",
                        )
                    result = await response.json()
                    return PaymentLimit(**result)
            except aiohttp.ClientError:
                log.error(
                    f"Error requesting operations rule from operations rule service. \
                    {self.host}/payment-limit/{user_id}"
                )
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


__all__ = ["OperationsRuleService"]
