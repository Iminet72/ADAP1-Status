"""Sensor platform for Ada1Status integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import Ada1StatusDataUpdateCoordinator
from .const import (
    DOMAIN,
    DEFAULT_NAME,
    TEXT_SENSOR_TYPES,
    NUMERIC_SENSOR_TYPES,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ada1Status sensors from a config entry."""
    coordinator: Ada1StatusDataUpdateCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]
    
    entities: list[SensorEntity] = []
    
    # Add text sensors
    for sensor_key in TEXT_SENSOR_TYPES:
        entities.append(Ada1StatusTextSensor(coordinator, sensor_key, config_entry))
    
    # Add numeric sensors
    for sensor_key in NUMERIC_SENSOR_TYPES:
        entities.append(Ada1StatusNumericSensor(coordinator, sensor_key, config_entry))
    
    async_add_entities(entities)


class Ada1StatusTextSensor(CoordinatorEntity[Ada1StatusDataUpdateCoordinator], SensorEntity):
    """Representation of an Ada1Status text sensor."""
    
    def __init__(
        self,
        coordinator: Ada1StatusDataUpdateCoordinator,
        sensor_key: str,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_key = sensor_key
        self._config_entry = config_entry
        
        sensor_info = TEXT_SENSOR_TYPES[sensor_key]
        self._attr_name = f"{DEFAULT_NAME} {sensor_info['name']}"
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
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        
        value = self.coordinator.data.get(self._sensor_key)
        return str(value) if value is not None else None
    
    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success


class Ada1StatusNumericSensor(CoordinatorEntity[Ada1StatusDataUpdateCoordinator], SensorEntity):
    """Representation of an Ada1Status numeric sensor."""
    
    def __init__(
        self,
        coordinator: Ada1StatusDataUpdateCoordinator,
        sensor_key: str,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_key = sensor_key
        self._config_entry = config_entry
        
        sensor_info = NUMERIC_SENSOR_TYPES[sensor_key]
        self._attr_name = f"{DEFAULT_NAME} {sensor_info['name']}"
        self._attr_native_unit_of_measurement = sensor_info["unit"]
        self._attr_device_class = sensor_info["device_class"]
        self._attr_state_class = sensor_info["state_class"]
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
    def native_value(self) -> float | int | None:
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        
        value = self.coordinator.data.get(self._sensor_key)
        if value is None:
            return None
        
        try:
            # Try to convert to numeric type
            if isinstance(value, (int, float)):
                return value
            return float(value)
        except (ValueError, TypeError):
            _LOGGER.warning(
                "Could not convert value '%s' for sensor '%s' to number",
                value,
                self._sensor_key,
            )
            return None
    
    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success
