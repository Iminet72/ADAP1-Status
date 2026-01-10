## Ada1Status - ADA-P1 Meter Integration

Monitor your ADA-P1 Meter device through Home Assistant.

### Features

- ⚡ Real-time sensor monitoring
- 🔌 Easy configuration through UI
- 🌍 Multi-language support (EN, HU)
- 📊 Multiple sensor types:
  - Voltage (V)
  - Current (A)
  - Power (W)
  - Energy (kWh)
  - Frequency (Hz)

### Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **Ada1Status**
4. Enter your ADA-P1 Meter IP address
5. Click **Submit**

### Device API

The integration expects a JSON response at `http://<device-ip>/status`:

```json
{
  "voltage": 230.5,
  "current": 5.2,
  "power": 1198.6,
  "energy": 1234.5,
  "frequency": 50.0
}
```

### Support

For issues and feature requests, visit the [GitHub repository](https://github.com/Iminet72/adaP1Status).
