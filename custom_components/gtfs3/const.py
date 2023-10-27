"""Constants for the Pronote integration."""

from homeassistant.const import Platform

DOMAIN = "gtfs3"

# default values for options
DEFAULT_REFRESH_INTERVAL=15

DEFAULT_NAME = "GTFS Sensor3"
DEFAULT_PATH = "gtfs3"

CONF_DATA = "data"
CONF_DESTINATION = "destination"
CONF_ORIGIN = "origin"
CONF_TOMORROW = "include_tomorrow"


PLATFORMS = [Platform.SENSOR]
