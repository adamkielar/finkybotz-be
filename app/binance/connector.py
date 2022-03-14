import hashlib
import hmac
import logging
import time
from dataclasses import dataclass
from typing import Any
from typing import Dict

from fastapi import HTTPException
from httpx import AsyncClient
from httpx import HTTPError
from httpx._types import HeaderTypes
from httpx._types import URLTypes

from app.binance.constants import RECV_WINDOW
from app.config import binance_settings

logger = logging.getLogger(__name__)


@dataclass
class BinanceConnectorBase:
    @property
    def recvwindow(self):
        return "recvWindow", RECV_WINDOW

    @property
    def timestamp(self):
        return "timestamp", round(time.time() * 1000)

    @classmethod
    async def _call(
        cls, url: URLTypes, method: str, headers: HeaderTypes, **kwargs
    ) -> Dict[str, Any]:
        async with AsyncClient() as client:
            try:
                response = await client.request(method, url, headers=headers, **kwargs)
                response.raise_for_status()
                return response.json()
            except HTTPError as exc:
                logger.error(f"Error while requesting {exc.request.url!r}.")
                raise HTTPException(
                    status_code=response.status_code, detail=response.json()
                )


@dataclass
class BinanceAuth:
    @property
    def binance_secret(self) -> str:
        return binance_settings.BINANCE_API_SECRET.get_secret_value()

    @property
    def headers(self) -> Dict[str, str]:
        return {"X-MBX-APIKEY": binance_settings.BINANCE_API_KEY.get_secret_value()}

    def sign_payload(self, payload: str) -> str:
        signature = hmac.new(
            self.binance_secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        return f"signature={signature}"


@dataclass
class BinanceConnector(BinanceConnectorBase, BinanceAuth):
    @property
    def endpoint(self):
        raise NotImplementedError()

    @property
    def url(self) -> str:
        return f"{binance_settings.BINANCE_HOST}/api/{binance_settings.BINANCE_API_VERSION}/{self.endpoint}"

    async def _get_data(self) -> Dict[str, Any]:
        return await self._call(
            url=self.url,
            method="get",
            headers=self.headers,
        )

    async def _send_data(
        self, method: str, data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        return await self._call(
            url=self.url,
            method=method,
            data=data,
            headers=self.headers,
        )

    async def get(self) -> Dict[str, Any]:
        return await self._get_data()
