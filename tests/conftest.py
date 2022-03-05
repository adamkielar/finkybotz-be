import pathlib
from typing import Generator

import pytest
from alembic import command
from alembic.config import Config
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.main import app
from database_interface.config import db_settings
from database_interface.config import db_url_settings
from database_interface.mssql.session import MssqlSessionManager
from tests.sql_templates import CLEAR_DB_SQL

APP_PATH = pathlib.Path(__file__).resolve().parents[1]

MIGRATIONS_PATH = str("/src/database_interface/migrations")


def get_alembic_config():
    alembic_config = Config("database_interface/alembic.ini")
    alembic_config.set_main_option("script_location", MIGRATIONS_PATH)
    alembic_config.set_main_option("sqlalchemy.url", db_url_settings.get_db_url())
    return alembic_config


def create_test_db() -> None:
    engine = create_engine(
        db_url_settings.get_db_url(), future=True
    )

    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
        connection.execute(text(f"DROP DATABASE IF EXISTS {db_settings.Test_DB_Name};"))
        connection.execute(
            text(f"CREATE DATABASE {db_settings.Test_DB_Name} COLLATE Polish_CI_AI;")
        )


def configure_database() -> None:
    alembic_config = get_alembic_config()
    print(alembic_config.get_main_option("script_location"))
    print(alembic_config.get_main_option("sqlalchemy.url"))
    command.upgrade(alembic_config, "head")


def unconfigure_database() -> None:
    alembic_config = get_alembic_config()
    command.downgrade(alembic_config, "base")


def pytest_configure(config):
    create_test_db()
    configure_database()


def pytest_unconfigure(config):
    unconfigure_database()


@pytest.fixture(autouse=True)
def db_session() -> Generator[Session, None, None]:
    with MssqlSessionManager() as session:
        yield session
        session.execute(text(CLEAR_DB_SQL))
        session.commit()
        session.close()


@pytest.fixture
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client
