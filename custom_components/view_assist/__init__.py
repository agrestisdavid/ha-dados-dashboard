"""View Assist custom integration."""

import logging

from homeassistant import config_entries
from homeassistant.const import CONF_TYPE
from homeassistant.core import HomeAssistant
from homeassistant.helpers import discovery_flow

from .const import DOMAIN
from .core import CoreManager
from .data import set_runtime_data_for_config
from .devices import DeviceManager
from .helpers import get_integration_entries, get_master_config_entry, is_first_instance
from .migration import async_migrate_view_assist_config_entry
from .typed import VAConfigEntry, VAType

_LOGGER = logging.getLogger(__name__)


def migrate_to_section(entry: VAConfigEntry, params: list[str]):
    """Build a section for the config entry."""
    section = {}
    for param in params:
        if entry.options.get(param):
            section[param] = entry.options.pop(param)
    return section


async def async_migrate_entry(
    hass: HomeAssistant,
    entry: VAConfigEntry,
) -> bool:
    """Migrate config entry if needed."""
    return await async_migrate_view_assist_config_entry(hass, entry)


async def async_setup_entry(hass: HomeAssistant, entry: VAConfigEntry):
    """Set up View Assist from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    has_master_entry = get_master_config_entry(hass)
    is_master_entry = has_master_entry and entry.data[CONF_TYPE] == VAType.MASTER_CONFIG

    if not has_master_entry:
        # Start a config flow to add a master entry if no master entry
        if is_first_instance(hass, entry):
            _LOGGER.debug("No master entry found, starting config flow")
            discovery_flow.async_create_flow(
                hass,
                DOMAIN,
                {"source": config_entries.SOURCE_INTEGRATION_DISCOVERY},
                {"name": VAType.MASTER_CONFIG},
            )
            return True
        return False

    # Set runtime data
    set_runtime_data_for_config(hass, entry, is_master_entry)

    if is_master_entry:
        # Load asset manager
        await CoreManager(hass, entry).async_start()
    else:
        # Load device manager
        await DeviceManager(hass, entry).async_setup()

    # Add config change listener
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    return True


async def _async_update_listener(hass: HomeAssistant, config_entry: VAConfigEntry):
    """Handle config options update."""
    # Reload the integration when the options change.
    hass.config_entries.async_schedule_reload(config_entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: VAConfigEntry):
    """Unload a config entry."""

    # Unload js resources
    if entry.data[CONF_TYPE] == VAType.MASTER_CONFIG:
        return await CoreManager.async_unload(hass, entry)
    return await DeviceManager.async_unload(hass, entry)
