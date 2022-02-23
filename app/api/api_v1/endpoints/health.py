from typing import Dict
from typing import Generator

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from database_interface.mssql.session import MssqlSessionManager

router = APIRouter()


async def get_mssql_session() -> Generator:
    with MssqlSessionManager() as mssql_db_session:
        yield mssql_db_session


@router.get("/mssql_db")
async def mssql_db_health(db_session: Session = Depends(get_mssql_session)) -> Dict[str, str]:
    db_version = db_session.execute(text("SELECT @@version")).scalar()
    return {"mssql version": db_version}
