"""Constants for the Ada1Status integration."""

DOMAIN = "ada1status"
DEFAULT_NAME = "ADA-P1 Meter"
DEFAULT_SCAN_INTERVAL = 30

# Configuration
CONF_HOST = "host"

# Sensor types
SENSOR_TYPES = {
    "voltage": {
        "name": "Voltage",
        "unit": "V",
        "icon": "mdi:flash",
        "device_class": "voltage",
    },
    "current": {
        "name": "Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
    },
    "power": {
        "name": "Power",
        "unit": "W",
        "icon": "mdi:lightning-bolt",
        "device_class": "power",
    },
    "energy": {
        "name": "Energy",
        "unit": "kWh",
        "icon": "mdi:counter",
        "device_class": "energy",
    },
    "frequency": {
        "name": "Frequency",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
        "device_class": "frequency",
    },
}
