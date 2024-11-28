"""Switch platform for brama_integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

from .const import DOMAIN, HtbMethod, MuteMethod, PowerMethod
from .entity import BramaIntegrationEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import BlueprintDataUpdateCoordinator
    from .data import BramaIntegrationConfigEntry

ENTITY_DESCRIPTIONS = (
    SwitchEntityDescription(
        key="power",
        name="Power",
        icon="mdi:power",
    ),
    SwitchEntityDescription(
        key="mute",
        name="Mute",
        icon="mdi:volume-off",
    ),
    SwitchEntityDescription(
        key="htb",
        name="Home Theater Bypass",
        icon="mdi:theater",
    ),
    SwitchEntityDescription(
        key="triode",
        name="Triode",
        icon="mdi:transistor",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: BramaIntegrationConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    async_add_entities(
        BramaIntegrationSwitch(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class BramaIntegrationSwitch(BramaIntegrationEntity, SwitchEntity):
    """brama_integration switch class."""

    def __init__(
        self,
        coordinator: BlueprintDataUpdateCoordinator,
        entity_description: SwitchEntityDescription,
    ) -> None:
        """Initialize the switch class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_{DOMAIN}_{entity_description.key}"
        )

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        if self.entity_description.key == "power":
            return self.coordinator.data.get("status", {}).get("amp_pwr", False)
        if self.entity_description.key == "mute":
            return self.coordinator.data.get("settings", {}).get("muted", False)
        if self.entity_description.key == "htb":
            return self.coordinator.data.get("settings", {}).get("htb", False)
        if self.entity_description.key == "triode":
            return self.coordinator.data.get("settings", {}).get("mix", 0)
        return False

    async def async_turn_on(self, **_: Any) -> None:
        """Turn on the switch."""
        if self.entity_description.key == "power":
            await self.coordinator.config_entry.runtime_data.client.async_set_power(
                PowerMethod.ON
            )
        elif self.entity_description.key == "mute":
            await self.coordinator.config_entry.runtime_data.client.async_set_muted(
                MuteMethod.MUTED
            )
        elif self.entity_description.key == "htb":
            await self.coordinator.config_entry.runtime_data.client.async_set_htb(
                HtbMethod.ENABLED
            )
        elif self.entity_description.key == "triode":
            await self.coordinator.config_entry.runtime_data.client.async_set_triode(1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **_: Any) -> None:
        """Turn off the switch."""
        if self.entity_description.key == "power":
            await self.coordinator.config_entry.runtime_data.client.async_set_power(
                PowerMethod.OFF
            )
        elif self.entity_description.key == "mute":
            await self.coordinator.config_entry.runtime_data.client.async_set_muted(
                MuteMethod.UNMUTED
            )
        elif self.entity_description.key == "htb":
            await self.coordinator.config_entry.runtime_data.client.async_set_htb(
                HtbMethod.DISABLED
            )
        elif self.entity_description.key == "triode":
            await self.coordinator.config_entry.runtime_data.client.async_set_triode(0)
        await self.coordinator.async_request_refresh()
