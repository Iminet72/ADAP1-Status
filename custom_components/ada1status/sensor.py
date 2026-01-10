"""Sensor platform for Ada1Status integration."""
import logging
from datetime import timedelta

import aiohttp

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, DEFAULT_NAME, DEFAULT_SCAN_INTERVAL, SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=DEFAULT_SCAN_INTERVAL)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ada1Status sensors from a config entry."""
    host = config_entry.data[CONF_HOST]
    
    coordinator = Ada1StatusCoordinator(hass, host)
    await coordinator.async_config_entry_first_refresh()

    entities = []
    for sensor_type in SENSOR_TYPES:
        entities.append(Ada1StatusSensor(coordinator, sensor_type, config_entry.entry_id))

    async_add_entities(entities)


class Ada1StatusCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Ada1Status data."""

    def __init__(self, hass: HomeAssistant, host: str) -> None:
        """Initialize."""
        self.host = host
        self.session = async_get_clientsession(hass)
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self):
        """Fetch data from ADA-P1 Meter."""
        try:
            async with self.session.get(
                self.host, timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status != 200:
                    raise UpdateFailed(f"HTTP {response.status}")
                
                text = await response.text()
                
                # Parse the data from the response
                # This is a simple parser that looks for key-value pairs
                data = {}
                for line in text.split('\n'):
                    line = line.strip()
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip().lower()
                        value = value.strip()
                        
                        # Try to convert to float
                        try:
                            # Remove units if present
                            value_clean = value.split()[0] if ' ' in value else value
                            data[key] = float(value_clean)
                        except (ValueError, IndexError):
                            data[key] = value
                
                return data
                
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err


class Ada1StatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of an Ada1Status sensor."""

    def __init__(
        self,
        coordinator: Ada1StatusCoordinator,
        sensor_type: str,
        entry_id: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._attr_name = f"{DEFAULT_NAME} {SENSOR_TYPES[sensor_type]['name']}"
        self._attr_unique_id = f"{entry_id}_{sensor_type}"
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type]["unit"]
        self._attr_icon = SENSOR_TYPES[sensor_type]["icon"]
        
        # Set device class and state class based on sensor type
        if sensor_type == "power":
            self._attr_device_class = SensorDeviceClass.POWER
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif sensor_type == "energy":
            self._attr_device_class = SensorDeviceClass.ENERGY
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        elif sensor_type == "voltage":
            self._attr_device_class = SensorDeviceClass.VOLTAGE
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif sensor_type == "current":
            self._attr_device_class = SensorDeviceClass.CURRENT
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif sensor_type == "frequency":
            self._attr_device_class = SensorDeviceClass.FREQUENCY
            self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        
        # Try to find the value in the coordinator data
        # Look for keys that match the sensor type
        for key in self.coordinator.data:
            if self._sensor_type in key:
                return self.coordinator.data[key]
        
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success
