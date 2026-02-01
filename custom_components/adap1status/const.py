"""Constants for the Adap1Status integration."""
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.const import (
    UnitOfDataRate,
    UnitOfTime,
    UnitOfInformation,
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
)

DOMAIN = "adap1status"
DEFAULT_NAME = "ADA-P1 Meter"
DEFAULT_SCAN_INTERVAL = 30
DEFAULT_PORT = 8989
TIMEOUT = 5

# Configuration
CONF_PORT = "port"
CONF_SCAN_INTERVAL = "scan_interval"

# Text sensor types
TEXT_SENSOR_TYPES = {
    "os_version": {
        "name": "OS Version",
        "icon": "mdi:information-outline",
    },
    "local_ip": {
        "name": "Local IP",
        "icon": "mdi:ip-network",
    },
    "hostname": {
        "name": "Hostname",
        "icon": "mdi:network",
    },
    "ssid": {
        "name": "SSID",
        "icon": "mdi:wifi",
    },
    "mqtt_server": {
        "name": "MQTT Server",
        "icon": "mdi:server-network",
    },
    "uptime_hhmm": {
        "name": "Uptime (HH:MM)",
        "icon": "mdi:clock-outline",
    },
}

# Numeric sensor types
NUMERIC_SENSOR_TYPES = {
    "wifi_rssi": {
        "name": "WiFi RSSI",
        "unit": SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        "device_class": SensorDeviceClass.SIGNAL_STRENGTH,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:wifi-strength-2",
    },
    "wifi_channel": {
        "name": "WiFi Channel",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:wifi-settings",
    },
    "serial_recent_sec": {
        "name": "Serial Recent",
        "unit": UnitOfTime.SECONDS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:serial-port",
    },
    "uptime_seconds": {
        "name": "Uptime",
        "unit": UnitOfTime.SECONDS,
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:timer-outline",
    },
    "heap_total": {
        "name": "Heap Total",
        "unit": UnitOfInformation.BYTES,
        "device_class": SensorDeviceClass.DATA_SIZE,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "heap_free": {
        "name": "Heap Free",
        "unit": UnitOfInformation.BYTES,
        "device_class": SensorDeviceClass.DATA_SIZE,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "heap_min_free": {
        "name": "Heap Min Free",
        "unit": UnitOfInformation.BYTES,
        "device_class": SensorDeviceClass.DATA_SIZE,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "heap_max_alloc": {
        "name": "Heap Max Alloc",
        "unit": UnitOfInformation.BYTES,
        "device_class": SensorDeviceClass.DATA_SIZE,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "heap_fragmentation": {
        "name": "Heap Fragmentation",
        "unit": PERCENTAGE,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:memory",
    },
    "fs_total": {
        "name": "Filesystem Total",
        "unit": UnitOfInformation.BYTES,
        "device_class": SensorDeviceClass.DATA_SIZE,
        "state_class": None,
        "icon": "mdi:harddisk",
    },
    "fs_used": {
        "name": "Filesystem Used",
        "unit": UnitOfInformation.BYTES,
        "device_class": SensorDeviceClass.DATA_SIZE,
        "state_class": None,
        "icon": "mdi:harddisk",
    },
    "watchdog_last_kick_ms": {
        "name": "Watchdog Last Kick",
        "unit": UnitOfTime.MILLISECONDS,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:timer-sand",
    },
    "chip_cores": {
        "name": "Chip Cores",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:chip",
    },
    "ack_items": {
        "name": "ACK Items",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:format-list-numbered",
    },
}

# Binary sensor types
BINARY_SENSOR_TYPES = {
    "mqtt_connected": {
        "name": "MQTT Connected",
        "device_class": BinarySensorDeviceClass.CONNECTIVITY,
        "icon": "mdi:server-network",
    },
    "telegram_url_mode": {
        "name": "Telegram URL Mode",
        "device_class": None,
        "icon": "mdi:telegram",
    },
    "telegram_url_set": {
        "name": "Telegram URL Set",
        "device_class": None,
        "icon": "mdi:telegram",
    },
    "rules_loaded": {
        "name": "Rules Loaded",
        "device_class": None,
        "icon": "mdi:script-text",
    },
    "watchdog_enabled": {
        "name": "Watchdog Enabled",
        "device_class": None,
        "icon": "mdi:shield-check",
    },
}
