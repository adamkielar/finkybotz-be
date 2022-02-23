from dataclasses import dataclass
from types import TracebackType
from typing import Optional
from typing import Type

import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from database_interface.config import db_engine_settings
from database_interface.config import db_url_settings

pyodbc.pooling = False

engine = create_engine(
    db_url_settings.get_db_url(), **db_engine_settings.mssql_settings()
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, future=True)


@dataclass
class MssqlSessionManager:
    def __post_init__(self) -> None:
        self.db_session = SessionLocal()

    def __enter__(self) -> Session:
        return self.db_session

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.db_session.close()

    async def __aenter__(self) -> Session:
        return self.db_session

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.db_session.close()
