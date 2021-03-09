"""Constants in AstroWeather component."""
import logging

from homeassistant.components.binary_sensor import DOMAIN as BINARY_SENSOR_DOMAIN
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN

DOMAIN = "astroweather"

CONF_FORECAST_INTERVAL = "forecast_interval"
CONF_LATITUDE = "latitude"
CONF_LONGITUDE = "longitude"
CONF_ELEVATION = "elevation"

ASTROWEATHER_PLATFORMS = [
    "binary_sensor",
    "sensor",
]

DEFAULT_ATTRIBUTION = "Powered by 7Timer"
DEFAULT_FORECAST_INTERVAL = 20
DEFAULT_ELEVATION = 0

LOGGER = logging.getLogger(__package__)
