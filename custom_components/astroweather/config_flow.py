""" Config Flow to configure AstroWeather Integration. """
import logging
import random
import string

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries, core
from homeassistant.const import (
    CONF_ID,
    CONF_LATITUDE,
    CONF_LONGITUDE,
)
from homeassistant.core import callback
from homeassistant.helpers import aiohttp_client
from homeassistant.util import slugify
from pyastroweatherio import AstroWeather, AstroWeatherError, RequestError, ResultError

from .const import (
    CONF_FORECAST_INTERVAL,
    DEFAULT_FORECAST_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class AstroWeatherFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a AstroWeather config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        if user_input is None:
            return await self._show_setup_form(user_input)

        unique_id = "".join(
            random.SystemRandom().choice(string.ascii_uppercase + string.digits)
            for _ in range(12)
        )

        _LOGGER.info(
            "Configured geolocation {}, {}".format(
                round(user_input[CONF_LATITUDE], 6),
                round(user_input[CONF_LONGITUDE], 6),
            )
        )
        return self.async_create_entry(
            title="{}, {}".format(
                round(user_input[CONF_LATITUDE], 6),
                round(user_input[CONF_LONGITUDE], 6),
            ),
            data={
                CONF_ID: unique_id,
                CONF_LATITUDE: user_input[CONF_LATITUDE],
                CONF_LONGITUDE: user_input[CONF_LONGITUDE],
                CONF_FORECAST_INTERVAL: user_input.get(CONF_FORECAST_INTERVAL),
            },
        )

    async def _show_setup_form(self, errors=None):
        """Show the setup form to the user."""

        latitude = self.hass.config.latitude
        longitude = self.hass.config.longitude

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_LATITUDE, default=latitude): vol.All(
                        vol.Coerce(float), vol.Range(min=-90, max=90)
                    ),
                    vol.Required(CONF_LONGITUDE, default=longitude): vol.All(
                        vol.Coerce(float), vol.Range(min=-180, max=180)
                    ),
                    vol.Optional(
                        CONF_FORECAST_INTERVAL, default=DEFAULT_FORECAST_INTERVAL
                    ): vol.All(vol.Coerce(int), vol.Range(min=5, max=60)),
                }
            ),
            errors=errors or {},
        )


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_FORECAST_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_FORECAST_INTERVAL, DEFAULT_FORECAST_INTERVAL
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=5, max=60)),
                }
            ),
        )
