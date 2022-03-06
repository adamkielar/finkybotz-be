from typing import AsyncGenerator
from typing import Dict

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.api_v1.prefixes import BINANCE_HEALTH_PREFIX
from app.api.api_v1.prefixes import DATABASE_HEALTH_PREFIX
from app.binance.connector import BinanceHealthEndpoint
from database_interface.mssql.session import MssqlSessionManager

router = APIRouter()


async def get_mssql_session() -> AsyncGenerator:
    with MssqlSessionManager() as mssql_db_session:
        yield mssql_db_session


@router.get(DATABASE_HEALTH_PREFIX)
async def mssql_db_health(
    db_session: Session = Depends(get_mssql_session),
) -> Dict[str, str]:
    db_version = db_session.execute(text("SELECT @@version")).scalar()
    return {"mssql version": db_version}


@router.get(BINANCE_HEALTH_PREFIX)
async def binance_health():
    status, response = BinanceHealthEndpoint().get()
    return {"status": status, "response": response}
