from fastapi import APIRouter

from app.api.api_v1.endpoints import health
from app.api.api_v1.prefixes import DATABASE_HEALTH_PREFIX

api_router = APIRouter()
api_router.include_router(health.router, tags=[DATABASE_HEALTH_PREFIX])
