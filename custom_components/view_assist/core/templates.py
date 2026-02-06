"""Adds template functions to HA."""

from __future__ import annotations

from collections.abc import Callable
import logging
from typing import Any

from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.template import Template, TemplateEnvironment

from ..helpers import (  # noqa: TID252
    get_config_entry_by_config_data_value,
    get_entities_by_attr_filter,
    get_mimic_entity_id,
    get_sensor_entity_from_instance,
)
from ..typed import VAConfigEntry  # noqa: TID252

DEFAULT_UNAVAILABLE_STATES = [
    STATE_UNKNOWN,
    STATE_UNAVAILABLE,
    "",
    None,
]

_LOGGER = logging.getLogger(__name__)


class TemplatesManager:
    """Class to manage template related functionality."""

    def __init__(self, hass: HomeAssistant, config: VAConfigEntry) -> None:
        """Initialize the TemplatesManager."""
        self.hass = hass
        self.config = config

    async def async_setup(self) -> bool:
        """Set up the TemplatesManager."""

        def is_safe_callable(self: TemplateEnvironment, obj) -> bool:
            return isinstance(
                obj,
                (ViewAssistEntities, ViewAssistEntity),
            ) or self.ct_original_is_safe_callable(obj)

        def patch_environment(env: TemplateEnvironment) -> None:
            env.globals["view_assist_entities"] = ViewAssistEntities(self.hass)
            env.globals["view_assist_entity"] = ViewAssistEntity(self.hass)

        def patched_init(
            self: TemplateEnvironment,
            hass_param: HomeAssistant | None,
            limited: bool | None = False,
            strict: bool | None = False,
            log_fn: Callable[[int, str], None] | None = None,
        ) -> None:
            self.ct_original__init__(hass_param, limited, strict, log_fn)
            patch_environment(self)

        if not hasattr(TemplateEnvironment, "ct_original__init__"):
            TemplateEnvironment.ct_original__init__ = TemplateEnvironment.__init__
            TemplateEnvironment.__init__ = patched_init

        if not hasattr(TemplateEnvironment, "ct_original_is_safe_callable"):
            TemplateEnvironment.ct_original_is_safe_callable = (
                TemplateEnvironment.is_safe_callable
            )
            TemplateEnvironment.is_safe_callable = is_safe_callable

        tpl = Template("", self.hass)
        tpl._strict = False  # noqa: SLF001
        tpl._limited = False  # noqa: SLF001
        patch_environment(tpl._env)  # noqa: SLF001
        tpl._strict = True  # noqa: SLF001
        tpl._limited = False  # noqa: SLF001
        patch_environment(tpl._env)  # noqa: SLF001

        return True

    async def async_unload(self) -> bool:
        """Unload the TemplatesManager."""
        return True


# Template functions
class ViewAssistEntities:
    """Get entities or attr by attr filter."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Init."""
        self._hass = hass

    def __call__(
        self,
        filter: dict[str, Any] | None = None,
        exclude: dict[str, Any] | None = None,
        attr: str | None = None,
    ) -> list[str]:
        "Call."
        entities = get_entities_by_attr_filter(self._hass, filter, exclude)
        if attr:
            return [
                self._hass.states.get(entity).attributes.get(attr)
                for entity in entities
            ]
        return entities

    def __repr__(self) -> str:
        """Print."""
        return "<template ViewAssistEntities>"


class ViewAssistEntity:
    """Gets a va entity id from the passed entity id or device id that matches any of theconfigured mic, mediaplyer, music player or display device."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Init."""
        self._hass = hass

    def __call__(self, param: str, mimic: bool = True) -> list[str]:
        "Call."
        if param is not None:
            if entry := get_config_entry_by_config_data_value(self._hass, param):
                return get_sensor_entity_from_instance(self._hass, entry.entry_id)
        if mimic:
            return get_mimic_entity_id(self._hass)
        return None

    def __repr__(self) -> str:
        """Print."""
        return "<template ViewAssistEntity>"
