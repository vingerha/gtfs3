"""Data update coordinator for the GTFS integration."""
from __future__ import annotations

from datetime import date, timedelta
from typing import Any

import logging
from .gtfs_helper import *
import re

import pygtfs
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.const import CONF_NAME, CONF_OFFSET, STATE_UNKNOWN


from .const import (
    DEFAULT_REFRESH_INTERVAL,
    DEFAULT_PATH
)

_LOGGER = logging.getLogger(__name__)

class GTFSUpdateCoordinator(DataUpdateCoordinator):
    """Data update coordinator for the Pronote integration."""
    _LOGGER.debug(f"coordinator: GTFSDataUpdate")
    config_entry: ConfigEntry

    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry
    ) -> None:
        """Initialize the coordinator."""
        _LOGGER.debug(f"coordinator: GTFSDataUpdate INIT")
        super().__init__(
            hass=hass,
            logger=_LOGGER,
            name=entry.title,
            update_interval=timedelta(minutes=entry.data.get("refresh_interval", DEFAULT_REFRESH_INTERVAL)),
        )
        self.config_entry = entry
        self.hass = hass
    async def _async_update_data(self) -> dict[Platform, dict[str, Any]]:
        """Get the latest data from GTFS and updates the state."""
        data = self.config_entry.data
        self._pygtfs = get_gtfs(self.hass, DEFAULT_PATH, data['file'])
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
            _LOGGER.info(
                "Error getting gtfs data from generic helper: %s", ex)            

        _LOGGER.debug(f"self.data: {self._data}")
        
        return self._data
