"""Platform for sensor integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

import aiohttp
import async_timeout

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL, SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=DEFAULT_SCAN_INTERVAL)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    host = config_entry.data[CONF_HOST]

    coordinator = Ada1StatusDataUpdateCoordinator(hass, host)
    await coordinator.async_config_entry_first_refresh()

    entities = []
    for sensor_type in SENSOR_TYPES:
        entities.append(Ada1StatusSensor(coordinator, sensor_type, config_entry))

    async_add_entities(entities)


class Ada1StatusDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the ADA-P1 Meter."""

    def __init__(self, hass: HomeAssistant, host: str) -> None:
        """Initialize."""
        self.host = host
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from ADA-P1 Meter."""
        url = f"http://{self.host}/status"
        
        try:
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status != 200:
                            raise UpdateFailed(f"Error communicating with device: {response.status}")
                        
                        data = await response.json()
                        return data
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with device: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}") from err


class Ada1StatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of an ADA-P1 Meter sensor."""

    def __init__(
        self,
        coordinator: Ada1StatusDataUpdateCoordinator,
        sensor_type: str,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._attr_name = f"{SENSOR_TYPES[sensor_type]['name']}"
        self._attr_unique_id = f"{config_entry.entry_id}_{sensor_type}"
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type]["unit"]
        self._attr_icon = SENSOR_TYPES[sensor_type]["icon"]
        
        # Set device class if available
        device_class = SENSOR_TYPES[sensor_type].get("device_class")
        if device_class == "voltage":
            self._attr_device_class = SensorDeviceClass.VOLTAGE
        elif device_class == "current":
            self._attr_device_class = SensorDeviceClass.CURRENT
        elif device_class == "power":
            self._attr_device_class = SensorDeviceClass.POWER
        elif device_class == "energy":
            self._attr_device_class = SensorDeviceClass.ENERGY
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        elif device_class == "frequency":
            self._attr_device_class = SensorDeviceClass.FREQUENCY

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        
        # Try to get the value from coordinator data
        # The actual key depends on what the ADA-P1 Meter returns
        return self.coordinator.data.get(self._sensor_type)

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self.coordinator.host)},
            "name": f"ADA-P1 Meter ({self.coordinator.host})",
            "manufacturer": "ADA",
            "model": "P1 Meter",
        }
