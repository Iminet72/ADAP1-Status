# Installation Guide

## Prerequisites

- Home Assistant 2023.1.0 or newer installed and running
- ADA-P1 Meter device connected to your network
- Network connectivity between Home Assistant and the ADA-P1 Meter

## Installation Steps

### Method 1: Manual Installation

1. **Download the Integration**
   - Download or clone this repository
   - Locate the `custom_components/ada1status` folder

2. **Copy to Home Assistant**
   - Navigate to your Home Assistant configuration directory (where `configuration.yaml` is located)
   - If it doesn't exist, create a `custom_components` directory
   - Copy the entire `ada1status` folder into `custom_components`
   
   Your directory structure should look like:
   ```
   homeassistant/
   ├── configuration.yaml
   └── custom_components/
       └── ada1status/
           ├── __init__.py
           ├── config_flow.py
           ├── const.py
           ├── manifest.json
           ├── sensor.py
           ├── strings.json
           └── translations/
               ├── en.json
               └── hu.json
   ```

3. **Restart Home Assistant**
   - Go to Settings → System → Restart
   - Wait for Home Assistant to fully restart

4. **Add the Integration**
   - Go to Settings → Devices & Services
   - Click the "+ ADD INTEGRATION" button (bottom right)
   - Search for "Ada1Status"
   - Click on it to start the configuration

5. **Configure the Device**
   - Enter the URL of your ADA-P1 Meter device
   - Examples:
     - `http://192.168.1.100`
     - `http://ada-p1-meter.local`
   - Click Submit

6. **Verify Installation**
   - The integration should now appear in your Devices & Services
   - You should see 5 new sensors created
   - Check the sensor values to ensure data is being received

### Method 2: HACS (Future)

This integration will be available through HACS in the future.

## Configuration Options

The integration currently supports the following configuration:

- **Device URL**: The HTTP address where your ADA-P1 Meter can be reached
  - Can be an IP address or hostname
  - Protocol (http:// or https://) is optional and will be added automatically if missing

## Sensors Created

After successful installation, the following sensors will be available:

- `sensor.ada_p1_meter_voltage` - Current voltage (V)
- `sensor.ada_p1_meter_current` - Current amperage (A)
- `sensor.ada_p1_meter_power` - Current power consumption (W)
- `sensor.ada_p1_meter_energy` - Total energy consumed (kWh)
- `sensor.ada_p1_meter_frequency` - Line frequency (Hz)

## Troubleshooting

### Integration doesn't appear in the list

- Make sure you copied the files to the correct location
- Restart Home Assistant again
- Check the Home Assistant logs for any errors related to `ada1status`

### Cannot connect to device

- Verify the device URL is correct
- Ensure the device is powered on and connected to the network
- Try accessing the URL from a web browser to confirm it's reachable
- Check your network firewall settings

### Sensors show "Unknown" or "Unavailable"

- Check the device URL is accessible
- Verify the device is responding with data
- Check the Home Assistant logs for specific error messages
- The integration expects data in a simple key:value format

### Viewing Logs

To see detailed logs for this integration:

1. Go to Settings → System → Logs
2. Search for "ada1status"
3. Look for any error or warning messages

Or enable debug logging by adding to `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.ada1status: debug
```

Then restart Home Assistant and check the logs again.

## Uninstallation

1. Go to Settings → Devices & Services
2. Find the Ada1Status integration
3. Click the three dots (⋮) and select "Delete"
4. Confirm the deletion
5. (Optional) Remove the `custom_components/ada1status` folder
6. (Optional) Restart Home Assistant
