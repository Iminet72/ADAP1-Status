"""Tests for the Adap1Status integration."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import aiohttp
import pytest

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.adap1status import (
    Adap1StatusDataUpdateCoordinator,
    async_setup_entry,
    async_unload_entry,
)
from custom_components.adap1status.const import (
    DOMAIN,
    DEFAULT_PORT,
    DEFAULT_SCAN_INTERVAL,
    CONF_PORT,
)


@pytest.fixture
def mock_config_entry():
    """Create a mock config entry."""
    return ConfigEntry(
        version=1,
        domain=DOMAIN,
        title="ADA-P1 Meter (192.168.1.100)",
        data={
            CONF_HOST: "192.168.1.100",
            CONF_PORT: DEFAULT_PORT,
            CONF_NAME: "Test Meter",
        },
        options={},
        source="user",
        entry_id="test_entry_id",
        unique_id="192.168.1.100",
    )


@pytest.fixture
def mock_status_data():
    """Create mock status data."""
    return {
        "os_version": "1.2.3",
        "local_ip": "192.168.1.100",
        "hostname": "ada-p1-meter",
        "ssid": "TestWiFi",
        "mqtt_server": "192.168.1.10",
        "mqtt_connected": True,
        "uptime_hhmm": "12:34",
        "uptime_seconds": 45240,
        "wifi_rssi": -65,
        "wifi_channel": 6,
        "serial_recent_sec": 5,
        "heap_total": 327680,
        "heap_free": 123456,
        "heap_min_free": 100000,
        "heap_max_alloc": 98304,
        "heap_fragmentation": 15,
        "fs_total": 1048576,
        "fs_used": 524288,
        "watchdog_enabled": True,
        "watchdog_last_kick_ms": 100,
        "telegram_url_mode": False,
        "telegram_url_set": True,
        "rules_loaded": True,
        "chip_cores": 2,
        "ack_items": 0,
    }


@pytest.mark.asyncio
async def test_coordinator_successful_update(hass: HomeAssistant, mock_status_data):
    """Test coordinator successfully fetches data."""
    from datetime import timedelta
    
    coordinator = Adap1StatusDataUpdateCoordinator(
        hass, "192.168.1.100", DEFAULT_PORT, timedelta(seconds=DEFAULT_SCAN_INTERVAL)
    )
    
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_status_data)
    
    with patch.object(coordinator.session, "get") as mock_get:
        mock_get.return_value.__aenter__.return_value = mock_response
        
        data = await coordinator._async_update_data()
        
        assert data == mock_status_data
        assert data["hostname"] == "ada-p1-meter"
        assert data["wifi_rssi"] == -65
        mock_get.assert_called_once()


@pytest.mark.asyncio
async def test_coordinator_http_error(hass: HomeAssistant):
    """Test coordinator handles HTTP errors."""
    from datetime import timedelta
    
    coordinator = Adap1StatusDataUpdateCoordinator(
        hass, "192.168.1.100", DEFAULT_PORT, timedelta(seconds=DEFAULT_SCAN_INTERVAL)
    )
    
    mock_response = AsyncMock()
    mock_response.status = 500
    
    with patch.object(coordinator.session, "get") as mock_get:
        mock_get.return_value.__aenter__.return_value = mock_response
        
        with pytest.raises(UpdateFailed) as exc_info:
            await coordinator._async_update_data()
        
        assert "HTTP 500" in str(exc_info.value)


@pytest.mark.asyncio
async def test_coordinator_timeout(hass: HomeAssistant):
    """Test coordinator handles timeout errors."""
    from datetime import timedelta
    
    coordinator = Adap1StatusDataUpdateCoordinator(
        hass, "192.168.1.100", DEFAULT_PORT, timedelta(seconds=DEFAULT_SCAN_INTERVAL)
    )
    
    with patch.object(coordinator.session, "get") as mock_get:
        mock_get.side_effect = aiohttp.ClientError("Timeout")
        
        with pytest.raises(UpdateFailed) as exc_info:
            await coordinator._async_update_data()
        
        assert "Error communicating with API" in str(exc_info.value)


@pytest.mark.asyncio
async def test_setup_entry(hass: HomeAssistant, mock_config_entry, mock_status_data):
    """Test setting up the integration."""
    hass.data[DOMAIN] = {}
    
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_status_data)
    
    with patch("custom_components.adap1status.async_get_clientsession") as mock_session:
        mock_session.return_value.get.return_value.__aenter__.return_value = mock_response
        
        with patch(
            "homeassistant.config_entries.ConfigEntries.async_forward_entry_setups"
        ) as mock_forward:
            result = await async_setup_entry(hass, mock_config_entry)
            
            assert result is True
            assert mock_config_entry.entry_id in hass.data[DOMAIN]
            assert isinstance(
                hass.data[DOMAIN][mock_config_entry.entry_id],
                Adap1StatusDataUpdateCoordinator,
            )
            mock_forward.assert_called_once()


@pytest.mark.asyncio
async def test_unload_entry(hass: HomeAssistant, mock_config_entry):
    """Test unloading the integration."""
    hass.data[DOMAIN] = {mock_config_entry.entry_id: AsyncMock()}
    
    with patch(
        "homeassistant.config_entries.ConfigEntries.async_unload_platforms",
        return_value=True,
    ):
        result = await async_unload_entry(hass, mock_config_entry)
        
        assert result is True
        assert mock_config_entry.entry_id not in hass.data[DOMAIN]


@pytest.mark.asyncio
async def test_sensor_availability_on_error(hass: HomeAssistant, mock_config_entry):
    """Test that sensors become unavailable when coordinator fails."""
    from datetime import timedelta
    from custom_components.adap1status.sensor import Adap1StatusTextSensor
    
    coordinator = Adap1StatusDataUpdateCoordinator(
        hass, "192.168.1.100", DEFAULT_PORT, timedelta(seconds=DEFAULT_SCAN_INTERVAL)
    )
    
    # Simulate failed update
    coordinator.last_update_success = False
    coordinator.data = None
    
    sensor = Adap1StatusTextSensor(coordinator, "hostname", mock_config_entry)
    
    assert sensor.available is False
    assert sensor.native_value is None


@pytest.mark.asyncio
async def test_binary_sensor_value_conversion(hass: HomeAssistant, mock_config_entry):
    """Test binary sensor value conversion."""
    from datetime import timedelta
    from custom_components.adap1status.binary_sensor import Adap1StatusBinarySensor
    
    coordinator = Adap1StatusDataUpdateCoordinator(
        hass, "192.168.1.100", DEFAULT_PORT, timedelta(seconds=DEFAULT_SCAN_INTERVAL)
    )
    
    # Test various true/false representations
    test_cases = [
        (True, True),
        (False, False),
        ("true", True),
        ("false", False),
        ("1", True),
        ("0", False),
        (1, True),
        (0, False),
    ]
    
    for value, expected in test_cases:
        coordinator.data = {"mqtt_connected": value}
        coordinator.last_update_success = True
        
        sensor = Adap1StatusBinarySensor(coordinator, "mqtt_connected", mock_config_entry)
        
        assert sensor.is_on == expected, f"Failed for value: {value}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
