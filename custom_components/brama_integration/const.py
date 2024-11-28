"""Constants for brama_integration."""

from enum import Enum
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "brama_integration"


class PowerMethod(Enum):
    """
    Enum setting the power state.

    Attributes:
        ON: Turn the power on.
        OFF: Turn the power off.

    """

    ON = 1
    OFF = 0


class MuteMethod(Enum):
    """
    Enum setting the mute state.

    Attributes:
        MUTED: Mute the audio.
        UNMUTED: Unmute the audio.

    """

    MUTED = 1
    UNMUTED = 0


class HtbMethod(Enum):
    """
    Enum setting the htb state.

    Attributes:
        ENABLED: Enable HTB.
        DISABLED: Disable HTB.

    """

    ENABLED = 1
    DISABLED = 0
