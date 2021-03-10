"""AstroWeather Integration for Home Assistant"""
import asyncio
import logging
from datetime import datetime, timedelta

import homeassistant.helpers.device_registry as dr
import voluptuous as vol
from aiohttp.client_exceptions import ServerDisconnectedError
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_ID
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.dispatcher import (
    async_dispatcher_connect,
    async_dispatcher_send,
)
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.typing import ConfigType, HomeAssistantType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pyastroweatherio import AstroWeather, AstroWeatherError, RequestError, ResultError

from .const import (
    ASTROWEATHER_PLATFORMS,
    DOMAIN,
    CONF_FORECAST_INTERVAL,
    DEFAULT_FORECAST_INTERVAL,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_ELEVATION,
    DEFAULT_ELEVATION,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistantType, config: ConfigType) -> bool:
    """Set up configured AstroWeather."""

    # We allow setup only through config flow type of config

    return True


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry) -> bool:
    """Set up AstroWeather platforms as config entry."""

    _LOGGER.debug("Starting up")

    if (
        not entry.options
        or not entry.options.get(CONF_LATITUDE)
        or not entry.options.get(CONF_LONGITUDE)
        or not entry.options.get(CONF_ELEVATION)
    ):
        hass.config_entries.async_update_entry(
            entry,
            options={
                CONF_FORECAST_INTERVAL: entry.data.get(
                    CONF_FORECAST_INTERVAL, DEFAULT_FORECAST_INTERVAL
                ),
                CONF_LATITUDE: entry.data[CONF_LATITUDE],
                CONF_LONGITUDE: entry.data[CONF_LONGITUDE],
                CONF_ELEVATION: entry.data.get(CONF_ELEVATION, DEFAULT_ELEVATION),
            },
        )

    session = async_get_clientsession(hass)

    # Apparently 7Timer has problems with a longitude of 0 degrees
    if entry.options.get(CONF_LONGITUDE) == 0:
        hass.config_entries.async_update_entry(
            entry,
            options={
                CONF_FORECAST_INTERVAL: entry.data.get(
                    CONF_FORECAST_INTERVAL, DEFAULT_FORECAST_INTERVAL
                ),
                CONF_LATITUDE: entry.data[CONF_LATITUDE],
                CONF_LONGITUDE: 0.000001,
                CONF_ELEVATION: entry.data.get(CONF_ELEVATION, DEFAULT_ELEVATION),
            },
        )

    _LOGGER.debug("Options Latitude " + str(entry.options.get(CONF_LATITUDE)))
    _LOGGER.debug("Options Longitude " + str(entry.options.get(CONF_LONGITUDE)))
    _LOGGER.debug("Options Elevation " + str(entry.options.get(CONF_ELEVATION)))

    astroweather = AstroWeather(
        session,
        entry.options.get(CONF_LATITUDE),
        entry.options.get(CONF_LONGITUDE),
        entry.options.get(CONF_ELEVATION),
    )
    _LOGGER.debug("Connected to AstroWeather Platform")

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = astroweather

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=astroweather.get_forecast,
        update_interval=timedelta(
            minutes=entry.options.get(CONF_FORECAST_INTERVAL, DEFAULT_FORECAST_INTERVAL)
        ),
    )
    _LOGGER.debug("Forecast Coordinator created")

    await coordinator.async_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "aw": astroweather,
    }

    _LOGGER.debug("Forecast updated")

    for platform in ASTROWEATHER_PLATFORMS:

        _LOGGER.debug("Creating " + str(platform))
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    if not entry.update_listeners:
        entry.add_update_listener(async_update_options)

    return True


async def async_update_options(hass: HomeAssistantType, entry: ConfigEntry):
    """Update options."""

    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistantType, entry: ConfigEntry) -> bool:
    """Unload config entry."""

    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in ASTROWEATHER_PLATFORMS
            ]
        )
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
