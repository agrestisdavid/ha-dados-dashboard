"""Number platform for Music Assistant Jukebox."""
from __future__ import annotations

from homeassistant.components.number import (
    NumberEntity,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers import state as state_helper
from homeassistant.helpers.restore_state import RestoreEntity

from .const import DOMAIN, LOGGER
from .switch import JukeboxBaseMixin

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up number platform."""
    async_add_entities([
        QueueLengthNumber(hass, entry),
        QueueDelayNumber(hass, entry)                
    ])

class QueueLengthNumber(JukeboxBaseMixin, NumberEntity):
    """Number entity for queue length."""

    _attr_has_entity_name = True
    _attr_name = "JukeBox: Queue length"
    _attr_unique_id = "jukebox_queue_length"
    _attr_native_unit_of_measurement = "tracks"
    _attr_icon = "mdi:playlist-music"
    _attr_native_min_value = 0
    _attr_native_max_value = 1000
    _attr_native_step = 1
    _attr_mode = NumberMode.BOX

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the number."""
        self.hass = hass
        self.entry = entry
        self._attr_native_value = 0

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        self._attr_native_value = int(value)
        self.async_write_ha_state()

class QueueDelayNumber(JukeboxBaseMixin, RestoreEntity, NumberEntity):
    """Number entity for queueing delay in seconds."""

    _attr_has_entity_name = True
    _attr_name = "JukeBox: Queuing Delay"
    _attr_unique_id = "jukebox_queuing_delay"
    _attr_native_unit_of_measurement = "seconds"
    _attr_icon = "mdi:timer"
    _attr_native_min_value = 0
    _attr_native_max_value = 300  # 5 minutes max
    _attr_native_step = 1
    _attr_mode = NumberMode.BOX

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the number."""
        self.hass = hass
        self.entry = entry
        self._attr_native_value = 0

    async def async_added_to_hass(self):
        """Restore last known value from state history."""
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()
        if last_state and last_state.state not in (None, "unknown", "unavailable"):
            try:
                self._attr_native_value = int(float(last_state.state))
                self.async_write_ha_state()
            except Exception:
                pass

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        self._attr_native_value = int(value)
        self.async_write_ha_state()
