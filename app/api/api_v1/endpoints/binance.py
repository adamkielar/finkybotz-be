from typing import Any
from typing import Dict

from fastapi import APIRouter
from fastapi import Path

from app.api.api_v1.prefixes import BINANCE_HEALTH
from app.api.api_v1.prefixes import BINANCE_SPOT_ACCOUNT
from app.api.api_v1.prefixes import BINANCE_SPOT_ACCOUNT_ALL_ORDERS
from app.api.api_v1.prefixes import BINANCE_SPOT_ACCOUNT_TRADE_LIST
from app.binance.handlers import BinanceHealthEndpoint
from app.binance.handlers import BinanceSpotAccountAllOrders
from app.binance.handlers import BinanceSpotAccountInformation
from app.binance.handlers import BinanceSpotAccountTradeList

router = APIRouter()


@router.get(BINANCE_HEALTH)
async def binance_health() -> Dict[str, Any]:

    return {"data": await BinanceHealthEndpoint().get()}


@router.get(BINANCE_SPOT_ACCOUNT)
async def binance_spot_account() -> Dict[str, Any]:
    """
    Get current account information.
    """

    return {"data": await BinanceSpotAccountInformation().get()}


@router.get(BINANCE_SPOT_ACCOUNT_TRADE_LIST)
async def binance_spot_account_trade_list(
    symbol: str = Path(..., title="Trading pair symbol")
) -> Dict[str, Any]:
    """
    Get trades for a specific account and symbol.
    """

    return {"data": await BinanceSpotAccountTradeList(symbol).get()}


@router.get(BINANCE_SPOT_ACCOUNT_ALL_ORDERS)
async def binance_spot_account_all_orders(
    symbol: str = Path(..., title="Trading pair symbol")
) -> Dict[str, Any]:
    """
    Get all account orders; active, canceled, or filled.
    """

    return {"data": await BinanceSpotAccountAllOrders(symbol).get()}
