"""Base Entity definition for AstroWeather Integration."""
import logging
from typing import Dict, List

from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.helpers.entity import Entity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class AstroWeatherEntity(Entity):
    """Base class for AstroWeather Entities."""

    def __init__(self, entries, entity, coordinator):
        """Initialize the AstroWeather Entity."""
        super().__init__()

        self.coordinator = coordinator
        self.entries = entries
        self._entity = entity
        self._unique_id = f"{self._entity}"

    @property
    def unique_id(self):
        """Return a unique ID."""

        return self._unique_id

    @property
    def _current(self):
        """Return Current Data."""

        return None

    @property
    def _forecast(self):
        """Return Forecast Data Array."""

        if self.coordinator is None:
            return None
        else:
            return self.coordinator.data[0]

    @property
    def available(self):
        """Return if entity is available."""

        return self.coordinator.last_update_success

    async def async_added_to_hass(self):
        """When entity is added to hass."""

        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
