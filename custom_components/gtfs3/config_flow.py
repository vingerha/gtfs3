"""Config flow for GTFS integration."""
from __future__ import annotations

import logging
from typing import Any
import uuid

import voluptuous as vol

#from datetime import time

from homeassistant import config_entries
from homeassistant.data_entry_flow import AbortFlow, FlowResult
from homeassistant.exceptions import HomeAssistantError
#from homeassistant.core import callback
from homeassistant.const import CONF_NAME, CONF_OFFSET, STATE_UNKNOWN
#from homeassistant.helpers import config_validation as cv

#from homeassistant.components.sensor import SensorEntity


from .gtfs_helper import *

from .const import (
    DOMAIN,
    DEFAULT_REFRESH_INTERVAL,
    DEFAULT_PATH,
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
        errors: dict[str, str] = {}
        if user_input is not None:
            _LOGGER.debug(f"Setup process initiated by user with user_input: {user_input} ")
            check_config = await self._check_config(user_input)
            if check_config:
                errors["base"] = check_config
            else:    
                return self.async_create_entry(title=user_input['name'], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_ROUTE, errors=errors
        )
        
    async def _check_config(self, data):
        self._pygtfs = get_gtfs(self.hass, DEFAULT_PATH, data['file'])
        if self._pygtfs == "no_data_file":
            return "no_data_file"
        self._data = {
            "schedule": self._pygtfs,
            "origin": data['origin'],
            "destination": data['destination'],
            "offset": data['offset'],
            "include_tomorrow": data['include_tomorrow'],
            "gtfs_dir": DEFAULT_PATH,
            "name": data['name'],            
            "next_departure": None,
        }
        try:
            self._data['next_departure'] = await self.hass.async_add_executor_job(get_next_departure, self._data)
        except Exception as ex:
            _LOGGER.info(f"Config: error getting gtfs data from generic helper: {ex}") 
            return "generic_failure"
        if self._data['next_departure']:
            return None
        else:
            return "stop_incorrect"
        
        

        
            
        

