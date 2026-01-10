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
    },
    "current": {
        "name": "Current",
        "unit": "A",
        "icon": "mdi:current-ac",
    },
    "power": {
        "name": "Power",
        "unit": "W",
        "icon": "mdi:power-plug",
    },
    "energy": {
        "name": "Energy",
        "unit": "kWh",
        "icon": "mdi:lightning-bolt",
    },
    "frequency": {
        "name": "Frequency",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
    },
}
