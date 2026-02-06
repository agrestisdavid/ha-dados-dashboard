"""Integration services."""

from __future__ import annotations

from asyncio import TimerHandle
import logging

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall, callback

from ..const import ATTR_EVENT_DATA, ATTR_EVENT_NAME, DOMAIN  # noqa: TID252
from ..typed import VAConfigEntry  # noqa: TID252

_LOGGER = logging.getLogger(__name__)


BROADCAST_EVENT_SERVICE_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_EVENT_NAME): str,
        vol.Required(ATTR_EVENT_DATA): dict,
    }
)


class Services:
    """Class to manage services."""

    def __init__(self, hass: HomeAssistant, config: VAConfigEntry) -> None:
        """Initialise."""
        self.hass = hass
        self.config = config

        self.navigate_task: dict[str, TimerHandle] = {}

    async def async_setup(self) -> bool:
        """Initialise VA services."""

        self.hass.services.async_register(
            DOMAIN,
            "broadcast_event",
            self._handle_broadcast_event,
            schema=BROADCAST_EVENT_SERVICE_SCHEMA,
        )
        return True

    async def async_unload(self) -> bool:
        """Stop the services."""
        self.hass.services.async_remove(DOMAIN, "broadcast_event")
        return True

    @callback
    def _handle_broadcast_event(self, call: ServiceCall):
        """Fire an event with the provided name and data.

        name: View Assist Broadcast Event
        description: Immediately fires an event with the provided name and data
        """
        event_name = call.data.get(ATTR_EVENT_NAME)
        event_data = call.data.get(ATTR_EVENT_DATA, {})
        # Fire the event
        self.hass.bus.fire(event_name, event_data)
