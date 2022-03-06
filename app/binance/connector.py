import hashlib
import hmac
from abc import ABC
from base64 import b64encode
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import Tuple

from httpx import AsyncClient
from httpx import HTTPError

from app.config import binance_settings


@dataclass
class BinanceConnectorBase:
    @property
    def endpoint(self):
        raise NotImplementedError()

    @property
    def url(self) -> str:
        return f"{binance_settings.BINANCE_HOST}/api/{binance_settings.BINANCE_API_VERSION}/{self.endpoint}"


@dataclass
class BinanceSignatureHandler:
    @property
    def message(self):
        raise NotImplementedError()

    @property
    def b64_binance_secret(self) -> bytes:
        return b64encode(binance_settings.BINANCE_API_SECRET.encode("ascii"))

    @property
    def signed_message(self):
        return hmac.new(
            self.b64_binance_secret, self.message.encode("ascii"), hashlib.sha256
        ).digest()


@dataclass
class BinanceConnector(BinanceConnectorBase, ABC):
    @classmethod
    async def _call(
        cls, url, method, headers, *args, **kwargs
    ) -> Tuple[int, Dict[str, Any]]:
        try:
            async with AsyncClient(headers=headers) as session:
                async with getattr(session, method)(url, *args, **kwargs) as response:
                    await response.raise_for_status()
                    return response.status, await response.json(content_type=None)
        except HTTPError as exc:
            print(f"Error while requesting {exc.request.url!r}.")

    async def _get_data(self, data=None, headers=None) -> Tuple[int, Dict[str, str]]:
        return await self._call(
            url=self.url,
            method="get",
            data=data,
            headers=headers,
        )

    async def _send_data(self, data=None, headers=None) -> Tuple[int, Dict[str, str]]:
        return await self._call(
            url=self.url,
            method="post",
            data=data,
            headers=headers,
        )


@dataclass
class BinanceHealthEndpoint(BinanceConnector):
    @property
    def endpoint(self):
        return "ping"

    async def get(self):
        response_status, response_json = await self._get_data()
        return response_status, response_json
