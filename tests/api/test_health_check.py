import pytest
from sqlalchemy import text
from starlette import status

from app.api.api_v1.prefixes import DATABASE_HEALTH_PREFIX


class TestHealthCheck:
    @pytest.mark.asyncio
    async def test_db(self, client, db_session):
        assert db_session.execute(text("SELECT 1")).scalar()
        response = await client.get(
            DATABASE_HEALTH_PREFIX,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
