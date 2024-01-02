"""Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """App settings."""
    OPERATIONS_RULE_MS_HOST: str
    ACCOUNT_MS_HOST: str
    TRANSACTION_MS_HOST: str

    CIRCUIT_BREAKER_FAILURE_THRESHOLD: int = 2
    CIRCUIT_BREAKER_RECOVERY_TIMEOUT: int = 30

    LOKI_ENDPOINT: str

    model_config = SettingsConfigDict(env_file=".env")


app_settings = AppSettings()


__all__ = ["app_settings", "AppSettings"]
