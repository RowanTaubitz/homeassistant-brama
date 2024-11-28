"""Selector platform for brama_integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.select import SelectEntity, SelectEntityDescription

from .const import DOMAIN
from .entity import BramaIntegrationEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import BlueprintDataUpdateCoordinator
    from .data import BramaIntegrationConfigEntry

# Define options and descriptions for selectors
ENTITY_DESCRIPTIONS = [
    SelectEntityDescription(
        key="input_selector",
        name="Input Selector",
        options=["Input 1", "Input 2", "Input 3", "Input 4", "Input 5"],
        icon="mdi:audio-input-xlr",
    ),
    SelectEntityDescription(
        key="backlight_selector",
        name="Backlight LED Level",
        options=["Off", "Low", "Medium", "High"],
        icon="mdi:led-on",
    ),
    SelectEntityDescription(
        key="gain_selector",
        name="Gain",
        options=["Low", "Medium", "High"],
        icon="mdi:volume-high",
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: BramaIntegrationConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the selector platform."""
    coordinator: BlueprintDataUpdateCoordinator = entry.runtime_data.coordinator

    async_add_entities(
        BramaIntegrationSelect(
            coordinator=coordinator, entity_description=entity_description
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class BramaIntegrationSelect(BramaIntegrationEntity, SelectEntity):
    """brama_integration select class."""

    def __init__(
        self,
        coordinator: BlueprintDataUpdateCoordinator,
        entity_description: SelectEntityDescription,
    ) -> None:
        """Initialize the select entity."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_{DOMAIN}_{entity_description.key}"
        )

    @property
    def current_option(self) -> str | None:
        """Return the current option for this selector."""
        if self.entity_description.key == "input_selector":
            input_index = self.coordinator.data.get("settings", {}).get("src", 0)
            return f"Input {input_index + 1}"
        if self.entity_description.key == "backlight_selector":
            level = self.coordinator.data.get("settings", {}).get("led_lvl", 0)
            if level is not None:
                return self.entity_description.options[level]  # type: ignore[index]
            return None
        if self.entity_description.key == "gain_selector":
            gain = self.coordinator.data.get("settings", {}).get("gain", 0)
            if gain is not None:
                return self.entity_description.options[gain]  # type: ignore[index]
        return None

    async def async_select_option(self, option: str) -> None:
        """Set the selected option."""
        if self.entity_description.key == "input_selector":
            if self.entity_description.options is not None:
                input_index = self.entity_description.options.index(option)
            else:
                input_index = 0
            await self.coordinator.config_entry.runtime_data.client.async_set_input(
                input_index
            )
            await self.coordinator.async_request_refresh()

        elif self.entity_description.key == "backlight_selector":
            if self.entity_description.options is not None:
                level = self.entity_description.options.index(option)
            else:
                level = 0
            await self.coordinator.config_entry.runtime_data.client.async_set_backlight(
                level
            )
            await self.coordinator.async_request_refresh()

        elif self.entity_description.key == "gain_selector":
            if self.entity_description.options is not None:
                gain = self.entity_description.options.index(option)
            else:
                gain = 0
            await self.coordinator.config_entry.runtime_data.client.async_set_gain(gain)
            await self.coordinator.async_request_refresh()
