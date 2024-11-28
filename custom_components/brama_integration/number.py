"""Number platform for brama_integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.number import NumberEntity, NumberEntityDescription
from homeassistant.const import PERCENTAGE

from .const import DOMAIN
from .entity import BramaIntegrationEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import BlueprintDataUpdateCoordinator
    from .data import BramaIntegrationConfigEntry

# Define the volume control entity
ENTITY_DESCRIPTIONS = [
    NumberEntityDescription(
        key="volume",
        name="Volume",
        icon="mdi:volume-high",
        native_min_value=0,
        native_max_value=100,
        native_step=1,
        native_unit_of_measurement=PERCENTAGE,
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: BramaIntegrationConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the number platform."""
    coordinator: BlueprintDataUpdateCoordinator = entry.runtime_data.coordinator

    async_add_entities(
        BramaIntegrationNumber(
            coordinator=coordinator, entity_description=entity_description
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class BramaIntegrationNumber(BramaIntegrationEntity, NumberEntity):
    """brama_integration number class."""

    def __init__(
        self,
        coordinator: BlueprintDataUpdateCoordinator,
        entity_description: NumberEntityDescription,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_{DOMAIN}_{entity_description.key}"
        )

    @property
    def native_value(self) -> float | None:
        """Return the current volume value."""
        return self.coordinator.data.get("settings", {}).get("vol", 0)

    async def async_set_native_value(self, value: float) -> None:
        """Set the volume to the specified value."""
        await self.coordinator.config_entry.runtime_data.client.async_set_volume(
            int(value)
        )
        await self.coordinator.async_request_refresh()
