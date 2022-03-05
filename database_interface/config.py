from typing import Any
from typing import Dict
from typing import Optional

from pydantic import BaseSettings
from pydantic import SecretStr
from sqlalchemy.engine import URL


class DbSettings(BaseSettings):
    Database: SecretStr
    Mssql_Server: SecretStr
    Environment: str
    ProjectName: str
    SQLAlchemyConnectionPoolLimit: int
    SQLAlchemyConnectionPoolOverflow: int
    SQLAlchemyConnectionTimeout: int
    Database_Dev_Url: Optional[str] = None
    Database_Test_Url: Optional[str] = None
    Test_DB_Name: str = "test_database"


db_settings = DbSettings()

PROJECT_NAME = db_settings.ProjectName
SQLALCHEMY_CONNECTION_POOL_LIMIT = int(db_settings.SQLAlchemyConnectionPoolLimit)
SQLALCHEMY_CONNECTION_POOL_OVERFLOW = int(db_settings.SQLAlchemyConnectionPoolOverflow)
SQLALCHEMY_CONNECTION_TIMEOUT = int(db_settings.SQLAlchemyConnectionTimeout)


class DBPoolEngineSettings:
    @staticmethod
    def mssql_settings() -> Dict[str, Any]:
        return {
            "pool_size": SQLALCHEMY_CONNECTION_POOL_LIMIT,
            "max_overflow": SQLALCHEMY_CONNECTION_POOL_OVERFLOW,
            "pool_pre_ping": True,
            "connect_args": {
                "connect_timeout": SQLALCHEMY_CONNECTION_TIMEOUT,
                "application_name": PROJECT_NAME,
            },
        }


db_engine_settings = DBPoolEngineSettings()


class DatabaseUrlSettings:
    @staticmethod
    def get_production_db_connection_string() -> str:
        return (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={db_settings.Mssql_Server};"
            f"DATABASE={db_settings.Database};"
            "Authentication=ActiveDirectoryMSI"
        )

    @staticmethod
    def get_develop_db_connection_string() -> Optional[str]:
        return db_settings.Database_Dev_Url

    @staticmethod
    def get_test_db_connection_string() -> Optional[str]:
        return db_settings.Database_Test_Url

    def get_db_url(self) -> Optional[str]:
        if db_settings.Environment == "dev":
            return self.get_develop_db_connection_string()
        if db_settings.Environment == "tst":
            return self.get_test_db_connection_string()
        return URL.create(
            "mssql+pyodbc",
            query={"odbc_connect": self.get_production_db_connection_string()},
        )


db_url_settings = DatabaseUrlSettings()
