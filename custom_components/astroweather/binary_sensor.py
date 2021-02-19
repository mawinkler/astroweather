"""
    Support for the AstroWeather from 7Timer
    This component will create a few binary sensors.

    For a full description, go here: https://github.com/mawinkler/astroweather

    Author: Markus Winkler
"""
import logging
from datetime import timedelta

try:
    from homeassistant.components.binary_sensor import (
        BinarySensorEntity as BinarySensorDevice,
    )
except ImportError:
    # Prior to HA v0.110
    from homeassistant.components.binary_sensor import BinarySensorDevice

from homeassistant.components.binary_sensor import ENTITY_ID_FORMAT
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION, CONF_ID
from homeassistant.helpers.entity import Entity, generate_entity_id
from homeassistant.helpers.typing import HomeAssistantType

from .const import DOMAIN
from .entity import AstroWeatherEntity

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = {
    "deep_sky_view": ["Deep Sky View", None, "mdi:weather-night", "mdi:weather-fog"],
}


async def async_setup_entry(
    hass: HomeAssistantType, entry: ConfigEntry, async_add_entities
) -> None:

    """Set up the 7Timer sensor platform."""
    _LOGGER.info("Set up 7Timer binary sensor platform")

    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    if not coordinator.data:
        return

    sensors = []
    for sensor in SENSOR_TYPES:
        sensors.append(AstroWeatherBinarySensor(entry.data, sensor, coordinator))
        _LOGGER.debug(f"Binary sensor added: {sensor}")

    async_add_entities(sensors, True)

    return True


class AstroWeatherBinarySensor(AstroWeatherEntity, BinarySensorDevice):
    """ Implementation of a AstroWeather Weatherflow Binary Sensor. """

    def __init__(self, entries, sensor, coordinator):
        """Initialize the sensor."""
        super().__init__(entries, sensor, coordinator)
        self._sensor = sensor
        self._device_class = SENSOR_TYPES[self._sensor][1]
        self._name = f"{DOMAIN.capitalize()} {SENSOR_TYPES[self._sensor][0]}"

    @property
    def name(self):
        """Return the name of the sensor."""

        return self._name

    @property
    def is_on(self):
        """Return the state of the sensor."""

        return getattr(self.coordinator.data[0], self._sensor) is True

    @property
    def icon(self):
        """Icon to use in the frontend."""

        return SENSOR_TYPES[self._sensor][1]
