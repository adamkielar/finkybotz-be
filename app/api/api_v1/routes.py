from fastapi import APIRouter

from app.api.api_v1.endpoints import binance
from app.api.api_v1.endpoints import health

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(binance.router, tags=["binance"])
