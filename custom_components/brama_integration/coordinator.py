"""DataUpdateCoordinator for brama_integration."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    BramaIntegrationApiClientError,
)
from .const import DOMAIN, LOGGER

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import BramaIntegrationConfigEntry


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class BlueprintDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: BramaIntegrationConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=5),
        )

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            # Fetch data from multiple endpoints
            status = (
                await self.config_entry.runtime_data.client.async_get_status()
            )  # Get status data
            settings = (
                await self.config_entry.runtime_data.client.async_get_settings()
            )  # Get settings data
            info = (
                await self.config_entry.runtime_data.client.async_get_info()
            )  # Get additional info data

            # Combine all data into a single dictionary
            data = {
                "status": status,
                "settings": settings,
                "info": info,
            }
        except BramaIntegrationApiClientError as exception:
            raise UpdateFailed(exception) from exception
        else:
            return data
