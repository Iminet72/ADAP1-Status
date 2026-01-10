# ADA-P1 Meter API Documentation

This document describes the expected HTTP API format from the ADA-P1 Meter device.

## Endpoint

The integration polls the base URL provided during configuration (e.g., `http://192.168.1.100`).

## Expected Response Format

The device should respond with plain text in a simple key-value format, with each measurement on a new line:

```
voltage: 230.5 V
current: 5.2 A
power: 1200 W
energy: 145.6 kWh
frequency: 50.0 Hz
```

### Format Specifications

- Each line contains a key-value pair separated by a colon (`:`)
- Keys should be lowercase and match the sensor types (voltage, current, power, energy, frequency)
- Values can include units (they will be stripped automatically)
- Whitespace before and after the colon is ignored
- Empty lines are ignored
- Comments or other text lines without a colon are ignored

### Alternative Formats

The parser is flexible and can handle variations:

```
voltage: 230.5
current: 5.2
power: 1200
energy: 145.6
frequency: 50.0
```

Or with different casing (will be converted to lowercase):

```
Voltage: 230.5 V
Current: 5.2 A
Power: 1200 W
Energy: 145.6 kWh
Frequency: 50.0 Hz
```

## HTTP Response Requirements

- **Status Code**: Must be `200 OK`
- **Content-Type**: `text/plain` (recommended) or `text/html`
- **Timeout**: The device should respond within 10 seconds

## Example HTTP Response

```http
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 98

voltage: 230.5 V
current: 5.2 A
power: 1200 W
energy: 145.6 kWh
frequency: 50.0 Hz
```

## Sensor Mapping

The integration will attempt to find values for each sensor type by looking for keys that contain the sensor name:

| Sensor Type | Looks for key containing | Unit | Description |
|-------------|-------------------------|------|-------------|
| voltage     | "voltage"               | V    | Electrical voltage |
| current     | "current"               | A    | Electrical current |
| power       | "power"                 | W    | Active power |
| energy      | "energy"                | kWh  | Total energy consumed |
| frequency   | "frequency"             | Hz   | Line frequency |

## Error Handling

If the device:
- Returns a non-200 status code → Integration will log an error and retry on next poll
- Times out (>10 seconds) → Integration will mark sensors as unavailable
- Returns unparseable data → Sensors will show `None` or last known value

## Testing Your Device

You can test if your device returns data in the correct format using curl:

```bash
curl http://192.168.1.100
```

The response should contain readable key-value pairs as described above.
