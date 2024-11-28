"""Sensor platform for brama_integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import UnitOfApparentPower, UnitOfTemperature

from .const import DOMAIN
from .entity import BramaIntegrationEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import BlueprintDataUpdateCoordinator
    from .data import BramaIntegrationConfigEntry

# Define sensor descriptions
ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="ac_voltage",
        name="AC Voltage",
        icon="mdi:flash",
        native_unit_of_measurement=UnitOfApparentPower.VOLT_AMPERE,
    ),
    SensorEntityDescription(
        key="temp_l",
        name="PA Left",
        icon="mdi:thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    SensorEntityDescription(
        key="temp_r",
        name="PA Right",
        icon="mdi:thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: BramaIntegrationConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        BramaIntegrationSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class BramaIntegrationSensor(BramaIntegrationEntity, SensorEntity):
    """brama_integration Sensor class."""

    def __init__(
        self,
        coordinator: BlueprintDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_{DOMAIN}_{entity_description.key}"
        )

    @property
    def native_value(self) -> float | int | str | None:
        """Return the native value of the sensor."""
        key = self.entity_description.key
        status = self.coordinator.data["status"]

        # Convert values if necessary (e.g., divide temperatures by 100)
        if key == "temp_l":
            return status.get(key, 0) / 100  # Convert from 1/100 °C to °C
        if key == "temp_r":
            return status.get(key, 0) / 100  # Convert from 1/100 °C to °C
        if key == "ac_voltage":
            return status.get("ac", 0) / 100  # Convert from 1/100 V to V
        return None
