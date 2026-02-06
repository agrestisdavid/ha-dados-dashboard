"""Image platform for music_assistant_jukebox."""
from __future__ import annotations

import os
import mimetypes
from datetime import datetime

from homeassistant.components.image import ImageEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, LOGGER

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up image entities based on a config entry."""
    entities = [
        JukeboxInternalQRCode(hass, entry),
        JukeboxExternalQRCode(hass, entry),
    ]
    async_add_entities(entities)

class JukeboxBaseMixin:
    """Mixin for common device info."""
    
    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, "jukebox")},
            name="Music Assistant Jukebox",
            manufacturer="DJS91 and TheOddPirate",
            model="Jukebox Controller",
            configuration_url="http://homeassistant.local:8123/local/jukebox/jukebox.html"
        )

class JukeboxInternalQRCode(JukeboxBaseMixin, ImageEntity):
    """Representation of the Jukebox Internal QR Code."""
    
    _attr_has_entity_name = True
    _attr_name = "Internal Access QR Code"
    _attr_unique_id = f"{DOMAIN}_internal_qr"
    
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the image entity."""
        self.hass = hass  # Set hass before calling super().__init__()
        self.entry = entry
        super().__init__(hass)
        self._attr_content_type = "image/png"
        self._image_path = hass.config.path("www/jukebox/internal_url_qr.png")
        self._attr_entity_picture = "/local/jukebox/internal_url_qr.png"
        self._load_image()

    def _load_image(self) -> None:
        """Load the image and set attributes."""
        if os.path.exists(self._image_path):
            self._attr_available = True
            self._attr_image_last_updated = datetime.fromtimestamp(os.path.getmtime(self._image_path))
            with open(self._image_path, "rb") as image_file:
                self._image = image_file.read()
        else:
            self._attr_available = False
            self._image = None

    async def async_image(self) -> bytes | None:
        """Return bytes of image."""
        return self._image

    @property
    def state(self) -> str:
        """Return state of image."""
        return "available" if self._attr_available else "unavailable"

class JukeboxExternalQRCode(JukeboxBaseMixin, ImageEntity):
    """Representation of the Jukebox External QR Code."""
    
    _attr_has_entity_name = True
    _attr_name = "External Access QR Code"
    _attr_unique_id = f"{DOMAIN}_external_qr"
    
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the image entity."""
        self.hass = hass  # Set hass before calling super().__init__()
        self.entry = entry
        super().__init__(hass)
        self._attr_content_type = "image/png"
        self._image_path = hass.config.path("www/jukebox/external_url_qr.png")
        self._attr_entity_picture = "/local/jukebox/external_url_qr.png"
        self._load_image()

    def _load_image(self) -> None:
        """Load the image and set attributes."""
        if os.path.exists(self._image_path):
            self._attr_available = True
            self._attr_image_last_updated = datetime.fromtimestamp(os.path.getmtime(self._image_path))
            with open(self._image_path, "rb") as image_file:
                self._image = image_file.read()
        else:
            self._attr_available = False
            self._image = None

    async def async_image(self) -> bytes | None:
        """Return bytes of image."""
        return self._image

    @property
    def state(self) -> str:
        """Return state of image."""
        return "available" if self._attr_available else "unavailable"  
