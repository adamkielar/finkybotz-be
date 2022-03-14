from dataclasses import dataclass
from typing import Any
from typing import List
from typing import Tuple
from urllib.parse import urlencode

from app.binance.connector import BinanceConnector


@dataclass
class BinanceHealthEndpoint(BinanceConnector):
    @property
    def endpoint(self):
        return "ping"


@dataclass
class BinanceSpotAccountInformation(BinanceConnector):
    """
    Get current account information.
    """

    @property
    def endpoint(self):
        query_params: List[Tuple[str, Any]] = [self.timestamp]
        return f"account?{urlencode(query_params)}&{self.sign_payload(urlencode(query_params))}"


@dataclass
class BinanceSpotAccountTradeList(BinanceConnector):
    """
    Get trades for a specific account and symbol.
    """

    symbol: str

    @property
    def endpoint(self):
        query_params: List[Tuple[str, Any]] = [("symbol", self.symbol), self.timestamp]
        return f"myTrades?{urlencode(query_params)}&{self.sign_payload(urlencode(query_params))}"


@dataclass
class BinanceSpotAccountAllOrders(BinanceConnector):
    """
    Get all account orders; active, canceled, or filled.
    """

    symbol: str
    startTime = None
    endTime = None

    @property
    def endpoint(self):
        query_params: List[Tuple[str, Any]] = [("symbol", self.symbol), self.timestamp]
        return f"allOrders?{urlencode(query_params)}&{self.sign_payload(urlencode(query_params))}"
