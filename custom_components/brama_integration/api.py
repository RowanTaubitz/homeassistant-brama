"""Sample API Client."""

from __future__ import annotations

import asyncio
import socket
from typing import Any

import aiohttp
import async_timeout

from .const import HtbMethod, MuteMethod, PowerMethod


class BramaIntegrationApiClientError(Exception):
    """Exception to indicate a general API error."""


class BramaIntegrationApiClientCommunicationError(
    BramaIntegrationApiClientError,
):
    """Exception to indicate a communication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    response.raise_for_status()


class BramaIntegrationApiClient:
    """Sample API Client."""

    def __init__(
        self,
        ip_address: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._ip_address = ip_address
        self._session = session
        self._base_url = f"http://{self._ip_address}/api"

    async def async_get(self, endpoint: str) -> Any:
        """Perform a GET request to the specified endpoint."""
        return await self._api_wrapper(method="get", url=f"{self._base_url}/{endpoint}")

    async def async_post(self, endpoint: str, data: dict) -> Any:
        """Perform a POST request to the specified endpoint."""
        return await self._api_wrapper(
            method="post",
            url=f"{self._base_url}/{endpoint}",
            data=data,
            headers={"Content-type": "application/json; charset=UTF-8"},
        )

    async def async_get_info(self) -> Any:
        """Get general info from the API."""
        return await self.async_get("info")

    async def async_get_settings(self) -> Any:
        """Get settings from the API."""
        return await self.async_get("settings")

    async def async_get_status(self) -> Any:
        """Get status from the API."""
        return await self.async_get("status")

    async def async_set_control(self, key: str, value: Any) -> Any:
        """Set a control parameter via the API."""
        return await self.async_post("control", data={"settings": {key: value}})

    # Specific setters using the generalized method
    async def async_set_power(self, value: PowerMethod) -> Any:
        """Set power state."""
        await self.async_post("control", {"power": value == PowerMethod.ON})
        return await asyncio.sleep(0.005)

    async def async_set_muted(self, value: MuteMethod) -> Any:
        """Set mute state."""
        return await self.async_set_control("muted", value)

    async def async_set_input(self, value: int) -> Any:
        """Set input source."""
        return await self.async_set_control("src", value)

    async def async_set_backlight(self, value: int) -> Any:
        """Set backlight level."""
        return await self.async_set_control("led_lvl", value)

    async def async_set_volume(self, value: int) -> Any:
        """Set volume level."""
        return await self.async_set_control("vol", value)

    async def async_set_htb(self, value: HtbMethod) -> Any:
        """Set HTB mode."""
        return await self.async_set_control("htb", value)

    async def async_set_triode(self, value: int) -> Any:
        """Set triode mix."""
        return await self.async_set_control("mix", value)

    async def async_set_gain(self, value: int) -> Any:
        """Set gain level."""
        return await self.async_set_control("gain", value)

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                _verify_response_or_raise(response)
                return await response.json(
                    content_type=None if method == "post" else "application/json"
                )

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise BramaIntegrationApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise BramaIntegrationApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise BramaIntegrationApiClientError(
                msg,
            ) from exception
