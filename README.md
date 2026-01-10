# Ada1Status - Home Assistant Integration

This is a custom Home Assistant integration for the ADA-P1 Meter device. It reads status information from the device via HTTP and displays it as sensors in Home Assistant.

## Features

- Automatic discovery and configuration via UI
- Real-time sensor data for:
  - Voltage (V)
  - Current (A)
  - Power (W)
  - Energy (kWh)
  - Frequency (Hz)
- Configurable polling interval (default: 30 seconds)
- Local polling - no cloud connection required

## Installation

### Manual Installation

1. Copy the `custom_components/ada1status` folder to your Home Assistant's `custom_components` directory
2. Restart Home Assistant
3. Add the integration via the UI:
   - Go to Settings → Devices & Services
   - Click "+ Add Integration"
   - Search for "Ada1Status"
   - Enter the URL of your ADA-P1 Meter device (e.g., `http://192.168.1.100`)

### HACS Installation (Future)

This integration can be added to HACS as a custom repository.

## Configuration

The integration is configured through the Home Assistant UI. You only need to provide:
- **Device URL**: The HTTP address of your ADA-P1 Meter (e.g., `http://192.168.1.100`)

## Sensors

Once configured, the integration will create the following sensors:

- `sensor.ada_p1_meter_voltage` - Current voltage
- `sensor.ada_p1_meter_current` - Current amperage
- `sensor.ada_p1_meter_power` - Current power consumption
- `sensor.ada_p1_meter_energy` - Total energy consumed
- `sensor.ada_p1_meter_frequency` - Line frequency

## Requirements

- Home Assistant 2023.1.0 or newer
- ADA-P1 Meter device accessible via HTTP
- Network connectivity between Home Assistant and the device

## Support

For issues, questions, or feature requests, please use the [GitHub Issues](https://github.com/Iminet72/adaP1Status/issues) page.

## License

This integration is provided as-is without any warranty.
