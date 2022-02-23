"""
    Support for the AstroWeather from 7Timer
    This component will create a few binary sensors.

    For a full description, go here: https://github.com/mawinkler/astroweather

    Author: Markus Winkler
"""
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.const import (
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_TIMESTAMP,
)
from .const import (
    DOMAIN,
)
from .entity import AstroWeatherEntity

SENSOR_NAME = 0
SENSOR_UNIT = 1
SENSOR_ICON = 2
SENSOR_DEVICE_CLASS = 3
SENSOR_STATE_CLASS = 4

STATE_CLASS_MEASUREMENT = "measurement"

_LOGGER = logging.getLogger(__name__)

# Sensor types are defined like: Name, Unit Type, icon, device class
SENSOR_TYPES = {
    "latitude": [
        "Latitude",
        "°",
        "mdi:latitude",
        None,
        None,
    ],
    "longitude": [
        "Longitude",
        "°",
        "mdi:longitude",
        None,
        None,
    ],
    "elevation": [
        "Elevation",
        "m",
        "mdi:image-filter-hdr",
        None,
        None,
    ],
    "timestamp": [
        "Timestamp",
        "",
        "mdi:calendar",
        DEVICE_CLASS_TIMESTAMP,
        None,
    ],
    "cloudcover_percentage": [
        "Clouds",
        "%",
        "mdi:weather-night-partly-cloudy",
        None,
        STATE_CLASS_MEASUREMENT,
    ],
    "cloudcover_plain": [
        "Clouds Plain",
        "",
        "mdi:weather-night-partly-cloudy",
        None,
        None,
    ],
    "seeing_percentage": [
        "Seeing",
        "%",
        "mdi:waves",
        None,
        STATE_CLASS_MEASUREMENT,
    ],
    "seeing_plain": [
        "Seeing Plain",
        "",
        "mdi:waves",
        None,
        None,
    ],
    "transparency_percentage": [
        "Transparency",
        "%",
        "mdi:safety-goggles",
        None,
        STATE_CLASS_MEASUREMENT,
    ],
    "transparency_plain": [
        "Transparency Plain",
        "mag",
        "mdi:safety-goggles",
        None,
        None,
    ],
    "lifted_index": [
        "Lifted Index",
        "°C",
        "mdi:arrow-expand-up",
        DEVICE_CLASS_TEMPERATURE,
        STATE_CLASS_MEASUREMENT,
    ],
    "lifted_index_plain": [
        "Lifted Index Plain",
        "",
        "mdi:arrow-expand-up",
        None,
        None,
    ],
    "rh2m": [
        "2m Relative Humidity",
        "%",
        "mdi:water-percent",
        DEVICE_CLASS_HUMIDITY,
        STATE_CLASS_MEASUREMENT,
    ],
    "wind10m_direction": [
        "10m Wind Direction",
        "",
        "mdi:weather-windy",
        None,
        None,
    ],
    "wind10m_speed": [
        "10m Wind Speed",
        "m/s",
        "mdi:windsock",
        None,
        STATE_CLASS_MEASUREMENT,
    ],
    "wind10m_speed_plain": [
        "10m Wind Speed Plain",
        "",
        "mdi:windsock",
        None,
        None,
    ],
    "temp2m": [
        "2m Temperature",
        "°C",
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
        STATE_CLASS_MEASUREMENT,
    ],
    "prec_type": [
        "Precipitation Type",
        "",
        "mdi:weather-snowy-rainy",
        None,
        None,
    ],
    "condition_percentage": [
        "Condition",
        "%",
        "mdi:weather-snowy-rainy",
        None,
        STATE_CLASS_MEASUREMENT,
    ],
    "sun_next_setting": [
        "Sun Next Setting",
        "",
        "mdi:weather-sunset-down",
        DEVICE_CLASS_TIMESTAMP,
        None,
    ],
    "sun_next_setting_astro": [
        "Sun Next Setting Astronomical",
        "",
        "mdi:weather-sunset-down",
        DEVICE_CLASS_TIMESTAMP,
        None,
    ],
    "sun_next_rising": [
        "Sun Next Rising",
        "",
        "mdi:weather-sunset-down",
        DEVICE_CLASS_TIMESTAMP,
        None,
    ],
    "sun_next_rising_astro": [
        "Sun Next Rising Astronomical",
        "",
        "mdi:weather-sunset-down",
        DEVICE_CLASS_TIMESTAMP,
        None,
    ],
    "moon_next_rising": [
        "Moon Next Rising",
        "",
        "mdi:arrow-up-circle-outline",
        DEVICE_CLASS_TIMESTAMP,
        None,
    ],
    "moon_next_setting": [
        "Moon Next Setting",
        "",
        "mdi:arrow-down-circle-outline",
        DEVICE_CLASS_TIMESTAMP,
        None,
    ],
    "moon_phase": [
        "Moon Phase",
        "%",
        "mdi:moon-waning-gibbous",
        None,
        None,
    ],
    "deepsky_forecast_today": [
        "Deepsky Forecast Today",
        "%",
        "mdi:calendar-star",
        None,
        None,
    ],
    "deepsky_forecast_today_plain": [
        "Deepsky Forecast Today Plain",
        "",
        "mdi:calendar-star",
        None,
        None,
    ],
    "deepsky_forecast_today_desc": [
        "Deepsky Forecast Today Description",
        "",
        "mdi:calendar-star",
        None,
        None,
    ],
    "deepsky_forecast_tomorrow": [
        "Deepsky Forecast Tomorrow",
        "%",
        "mdi:calendar-star",
        None,
        None,
    ],
    "deepsky_forecast_tomorrow_plain": [
        "Deepsky Forecast Tomorrow Plain",
        "",
        "mdi:calendar-star",
        None,
        None,
    ],
    "deepsky_forecast_tomorrow_desc": [
        "Deepsky Forecast Tomorrow Description",
        "",
        "mdi:calendar-star",
        None,
        None,
    ],
}


async def async_setup_entry(
    hass: HomeAssistantType, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up the AstroWeather sensor platform."""
    _LOGGER.info("Set up AstroWeather sensor platform")

    fcst_coordinator = hass.data[DOMAIN][entry.entry_id]["fcst_coordinator"]
    if not fcst_coordinator.data:
        return False

    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    if not coordinator.data:
        return False

    astroweather = hass.data[DOMAIN][entry.entry_id]["aw"]
    if not astroweather:
        return False

    sensors = []
    for sensor in SENSOR_TYPES:
        sensors.append(
            AstroWeatherSensor(coordinator, entry.data, sensor, fcst_coordinator)
        )

    async_add_entities(sensors, True)
    return True


class AstroWeatherSensor(AstroWeatherEntity, SensorEntity):
    """Implementation of a AstroWeather Weatherflow Sensor."""

    def __init__(self, coordinator, entries, sensor, fcst_coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator, entries, sensor, fcst_coordinator)
        self._sensor = sensor
        self._state = None
        self._name = f"{DOMAIN.capitalize()} {SENSOR_TYPES[self._sensor][SENSOR_NAME]}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return getattr(self.coordinator.data[SENSOR_NAME], self._sensor, None)

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return SENSOR_TYPES[self._sensor][SENSOR_UNIT]

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return SENSOR_TYPES[self._sensor][SENSOR_ICON]

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return SENSOR_TYPES[self._sensor][SENSOR_DEVICE_CLASS]

    @property
    def state_class(self) -> str:
        """State class of sensor."""
        return SENSOR_TYPES[self._sensor][SENSOR_STATE_CLASS]
