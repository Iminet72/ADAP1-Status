"""Binary sensor platform for Adap1Status integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import Adap1StatusDataUpdateCoordinator
from .const import DOMAIN, DEFAULT_NAME, BINARY_SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Adap1Status binary sensors from a config entry."""
    coordinator: Adap1StatusDataUpdateCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]
    
    entities: list[BinarySensorEntity] = []
    
    # Add binary sensors
    for sensor_key in BINARY_SENSOR_TYPES:
        entities.append(Adap1StatusBinarySensor(coordinator, sensor_key, config_entry))
    
    async_add_entities(entities)


class Adap1StatusBinarySensor(
    CoordinatorEntity[Adap1StatusDataUpdateCoordinator], BinarySensorEntity
):
    """Representation of an Adap1Status binary sensor."""
    
    def __init__(
        self,
        coordinator: Adap1StatusDataUpdateCoordinator,
        sensor_key: str,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._sensor_key = sensor_key
        self._config_entry = config_entry
        
        sensor_info = BINARY_SENSOR_TYPES[sensor_key]
        self._attr_name = f"{DEFAULT_NAME} {sensor_info['name']}"
        self._attr_device_class = sensor_info["device_class"]
        self._attr_icon = sensor_info["icon"]
        
        # Get hostname from coordinator data for unique_id and device info
        hostname = self._get_hostname()
        self._attr_unique_id = f"{hostname}_{sensor_key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, hostname)},
            name=DEFAULT_NAME,
            manufacturer="ADA",
            model="ADA-P1Meter",
        )
    
    def _get_hostname(self) -> str:
        """Get hostname from coordinator data or fall back to host."""
        if self.coordinator.data and "hostname" in self.coordinator.data:
            return str(self.coordinator.data["hostname"])
        return self._config_entry.data[CONF_HOST]
    
    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        if self.coordinator.data is None:
            return None
        
        value = self.coordinator.data.get(self._sensor_key)
        if value is None:
            return None
        
        # Convert various true/false representations to boolean
        if isinstance(value, bool):
            return value
        
        if isinstance(value, str):
            return value.lower() in ("true", "1", "on", "yes")
        
        if isinstance(value, (int, float)):
            return bool(value)
        
        return None
    
    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success
