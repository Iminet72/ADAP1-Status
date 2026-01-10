# Ada1Status - Home Assistant Integration

Home Assistant custom integration for ADA-P1 Meter devices.

## Description

This integration allows you to monitor your ADA-P1 Meter device status through Home Assistant. It reads data from the device via HTTP and displays it as sensors.

## Features

- Automatic device discovery via config flow
- Real-time sensor data updates
- Multiple sensor types:
  - Voltage (V)
  - Current (A)
  - Power (W)
  - Energy (kWh)
  - Frequency (Hz)
- 30-second polling interval
- Multi-language support (English, Hungarian)

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/Iminet72/adaP1Status`
6. Select category: "Integration"
7. Click "Add"
8. Find "Ada1Status" in the integration list and install it
9. Restart Home Assistant

### Manual Installation

1. Download the `custom_components/ada1status` folder from this repository
2. Copy it to your Home Assistant's `custom_components` directory
3. Restart Home Assistant

## Configuration

1. Go to Settings → Devices & Services
2. Click "+ Add Integration"
3. Search for "Ada1Status"
4. Enter your ADA-P1 Meter device IP address or hostname
5. Click "Submit"

The integration will create sensors for all available measurements.

## Device API

The integration expects the ADA-P1 Meter to provide a JSON response at `http://<device-ip>/status` with the following structure:

```json
{
  "voltage": 230.5,
  "current": 5.2,
  "power": 1198.6,
  "energy": 1234.5,
  "frequency": 50.0
}
```

## Support

For issues and feature requests, please use the [GitHub issue tracker](https://github.com/Iminet72/adaP1Status/issues).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
