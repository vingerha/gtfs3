"""Config flow for GTFS integration."""
from __future__ import annotations

import logging
from typing import Any
import uuid

import voluptuous as vol

from datetime import time

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.core import callback
from homeassistant.const import CONF_NAME, CONF_OFFSET, STATE_UNKNOWN
from homeassistant.helpers import config_validation as cv

from homeassistant.components.sensor import SensorEntity


from .gtfs_helper import *

from .const import (
    DOMAIN,
    DEFAULT_REFRESH_INTERVAL,
)


_LOGGER = logging.getLogger(__name__)


STEP_USER_ROUTE = vol.Schema(
    {
        vol.Required("name"): str,
        vol.Required("origin"): str,
        vol.Required("destination"): str,
        vol.Optional("offset", default = 0): int,
        vol.Required("refresh_interval", default = 15): int,
        vol.Required("file"): str,
        vol.Required("include_tomorrow"): vol.In({'no': 'No', 'yes': 'Yes'})
    }
)

@config_entries.HANDLERS.register(DOMAIN)
class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Pronote."""
    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle a flow initialized by the user."""
        _LOGGER.debug("Setup process initiated by user with offset: {CONF_OFFSET} ")
        if user_input is None:
            _LOGGER.info("Selecting route")

            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_ROUTE
            )
        return self.async_create_entry(title=user_input['name'], data=user_input)

class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
