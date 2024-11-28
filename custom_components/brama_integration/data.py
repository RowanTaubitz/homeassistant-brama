"""Custom types for brama_integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import BramaIntegrationApiClient
    from .coordinator import BlueprintDataUpdateCoordinator


type BramaIntegrationConfigEntry = ConfigEntry[BramaIntegrationData]


@dataclass
class BramaIntegrationData:
    """Data for the Blueprint integration."""

    client: BramaIntegrationApiClient
    coordinator: BlueprintDataUpdateCoordinator
    integration: Integration
