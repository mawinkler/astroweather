"""
    Support for the AstroWeather from 7Timer
    This component will create a few binary sensors.

    For a full description, go here: https://github.com/mawinkler/astroweather

    Author: Markus Winkler
"""
import logging
from typing import Dict

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.util import slugify
from typing import Dict, List

from .const import (
    DOMAIN,
)
from .entity import AstroWeatherEntity

_LOGGER = logging.getLogger(__name__)

# Sensor types are defined like: Name, Unit Type, icon, device class
SENSOR_TYPES = {
    "latitude": [
        "Latitude",
        "°",
        "mdi:latitude",
        None,
    ],
    "longitude": [
        "Longitude",
        "°",
        "mdi:longitude",
        None,
    ],
    "timestamp": [
        "Timestamp",
        "",
        "mdi:calendar",
        None,
    ],
    "cloudcover": [
        "Clouds",
        "",
        "mdi:weather-night-partly-cloudy",
        None,
    ],
    "cloudcover_plain": [
        "Clouds Plain",
        "%",
        "mdi:weather-night-partly-cloudy",
        None,
    ],
    "seeing": [
        "Seeing",
        "",
        "mdi:waves",
        None,
    ],
    "seeing_plain": [
        "Seeing Plain",
        "\"",
        "mdi:waves",
        None,
    ],
    "transparency": [
        "Transparency",
        "",
        "mdi:safety-goggles",
        None,
    ],
    "transparency_plain": [
        "Transparency Plain",
        "mag",
        "mdi:safety-goggles",
        None,
    ],
    "lifted_index": [
        "Lifted Index",
        "",
        "mdi:arrow-expand-up",
        None,
    ],
    "lifted_index_plain": [
        "Lifted Index Plain",
        "°",
        "mdi:arrow-expand-up",
        None,
    ],
    "rh2m": [
        "2m Relative Humidity",
        "",
        "mdi:water-percent",
        None,
    ],
    "rh2m_plain": [
        "2m Relative Humidity Plain",
        "%",
        "mdi:water-percent",
        None,
    ],
    "wind10m_direction": [
        "10m Wind Direction",
        "",
        "mdi:weather-windy",
        None,
    ],
    "wind10m_speed": [
        "10m Wind Speed",
        "",
        "mdi:windsock",
        None,
    ],
    "wind10m_speed_plain": [
        "10m Wind Speed Plain",
        "",
        "mdi:windsock",
        None,
    ],
    "temp2m": [
        "2m Temperature",
        "°C",
        "mdi:thermometer",
        None,
    ],
    "prec_type": [
        "Precipitation Type",
        "",
        "mdi:weather-snowy-rainy",
        None,
    ],
    "view_condition": [
        "View Condition",
        "",
        "mdi:weather-snowy-rainy",
        None,
    ],
    "view_condition_plain": [
        "View Condition Plain",
        "",
        "mdi:weather-snowy-rainy",
        None,
    ],
    "forecast0": [
        "Forecast Today",
        "",
        "mdi:calendar-star",
        None,
    ],
    "forecast0_plain": [
        "Forecast Today Plain",
        "",
        "mdi:calendar-star",
        None,
    ],
    "forecast1": [
        "Forecast Tomorrow",
        "",
        "mdi:calendar-star",
        None,
    ],
    "forecast1_plain": [
        "Forecast Tomorrow Plain",
        "",
        "mdi:calendar-star",
        None,
    ],
    "sun_next_setting": [
        "Sun Next Setting",
        "",
        "mdi:weather-sunset-down",
        None,
    ],
    "moon_next_rising": [
        "Moon Next Rising",
        "",
        "mdi:arrow-top-right-thick",
        None,
    ],
    "moon_next_setting": [
        "Moon Next Setting",
        "",
        "mdi:arrow-bottom-right-thick",
        None,
    ],
    "moon_phase": [
        "Moon Phase",
        "%",
        "mdi:moon-waning-gibbous",
        None,
    ],
}


async def async_setup_entry(
    hass: HomeAssistantType, entry: ConfigEntry, async_add_entities
) -> None:

    """Set up the 7Timer sensor platform."""
    _LOGGER.info("Set up 7Timer sensor platform")

    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    if not coordinator.data:
        return

    astroweather = hass.data[DOMAIN][entry.entry_id]["aw"]
    if not astroweather:
        return

    sensors = []
    for sensor in SENSOR_TYPES:
        sensors.append(
            AstroWeatherSensor(
                entry.data,
                sensor,
                coordinator,
            )
        )

        _LOGGER.debug(f"Sensor added: {sensor}")

    async_add_entities(sensors, True)
    return True


class AstroWeatherSensor(AstroWeatherEntity, Entity):
    """ Implementation of a AstroWeather Weatherflow Sensor. """

    def __init__(
        self,
        entries,
        sensor,
        coordinator,
    ):

        """Initialize the sensor."""
        super().__init__(
            entries,
            sensor,
            coordinator,
        )
        self._sensor = sensor
        self._state = None
        self._name = f"{DOMAIN.capitalize()} {SENSOR_TYPES[self._sensor][0]}"

    @property
    def name(self):
        """Return the name of the sensor."""

        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""

        return getattr(self.coordinator.data[0], self._sensor, None)

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""

        return SENSOR_TYPES[self._sensor][1]

    @property
    def icon(self):
        """Icon to use in the frontend."""

        return SENSOR_TYPES[self._sensor][2]

    @property
    def device_class(self):
        """Return the device class of the sensor."""

        return SENSOR_TYPES[self._sensor][3]

    @property
    def forecast(self) -> List:
        """Return the forecast."""
        if self.coordinator.data is None or len(self.coordinator.data) < 2:
            return None

        data = []

        for forecast in self.coordinator.data:

            _LOGGER.debug(f"Forecast: {forecast.cloudcover}")
            data.append({"cloudcover": forecast.cloudcover})

        return data
