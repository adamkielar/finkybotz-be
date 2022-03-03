import secrets

from pydantic import BaseSettings


class AppSettings(BaseSettings):
    DEBUG: bool = False
    PROJECT_NAME: str = "FinkyBotz"
    SECRET_KEY: str = secrets.token_urlsafe(32)


settings = AppSettings()
