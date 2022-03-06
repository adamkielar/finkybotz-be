import secrets

from pydantic import BaseSettings
from pydantic import SecretStr


class AppSettings(BaseSettings):
    DEBUG: bool = False
    PROJECT_NAME: str = "FinkyBotz"
    SECRET_KEY: str = secrets.token_urlsafe(32)


class BinanceApiSettings(BaseSettings):
    BINANCE_API_KEY: SecretStr = None
    BINANCE_API_SECRET: SecretStr = None
    BINANCE_API_VERSION: str = "v3"
    BINANCE_HOST: str = "https://api.binance.com"


settings = AppSettings()
binance_settings = BinanceApiSettings()
