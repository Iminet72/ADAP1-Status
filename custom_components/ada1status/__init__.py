"""The Ada1Status integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    DOMAIN,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_PORT,
    TIMEOUT,
    CONF_PORT,
    CONF_SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Ada1Status from a config entry."""
    host = entry.data[CONF_HOST]
    port = entry.data.get(CONF_PORT, DEFAULT_PORT)
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    
    coordinator = Ada1StatusDataUpdateCoordinator(
        hass, host, port, timedelta(seconds=scan_interval)
    )
    
    await coordinator.async_config_entry_first_refresh()
    
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Set up options update listener
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry when options change."""
    await hass.config_entries.async_reload(entry.entry_id)


class Ada1StatusDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching Ada1Status data from JSON API."""
    
    def __init__(
        self,
        hass: HomeAssistant,
        host: str,
        port: int,
        update_interval: timedelta,
    ) -> None:
        """Initialize the coordinator."""
        self.host = host
        self.port = port
        self.session = async_get_clientsession(hass)
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )
    
    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from ADA-P1 Meter JSON API."""
        url = f"http://{self.host}:{self.port}/status"
        
        try:
            async with self.session.get(
                url, timeout=aiohttp.ClientTimeout(total=TIMEOUT)
            ) as response:
                if response.status != 200:
                    raise UpdateFailed(f"HTTP {response.status} from {url}")
                
                data = await response.json()
                _LOGGER.debug("Successfully fetched data from %s: %s", url, data)
                return data
                
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with API at {url}: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Unexpected error fetching data from {url}: {err}") from err
