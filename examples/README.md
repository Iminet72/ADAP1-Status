# Examples

This directory contains example scripts and utilities for testing the Ada1Status integration.

## Mock Server

`mock_server.py` - A simple HTTP server that simulates an ADA-P1 Meter device.

### Usage

```bash
python3 examples/mock_server.py
```

This will start a server on `http://localhost:8080` that returns simulated sensor data.

You can then add the integration in Home Assistant using the URL: `http://localhost:8080` (or `http://<your-ha-ip>:8080` if running on the same machine as Home Assistant).

### What it does

- Responds to HTTP GET requests with simulated sensor data
- Returns realistic values for voltage, current, power, energy, and frequency
- Values change slightly on each request to simulate real measurements
- Energy value increases over time
- Logs all requests to the console

### Testing scenarios

You can modify the script to test different scenarios:

1. **Connection errors**: Stop the server to test unavailable device handling
2. **Invalid data**: Modify the response format to test parsing
3. **Timeout**: Add delays in the `do_GET` method to test timeout handling
4. **Different values**: Adjust the random ranges or base values

### Example output

```
Mock ADA-P1 Meter server running on http://localhost:8080
Configure Home Assistant integration with: http://localhost:8080
Press Ctrl+C to stop
[10/Jan/2026 17:30:45] GET / HTTP/1.1 200 -
[10/Jan/2026 17:31:15] GET / HTTP/1.1 200 -
```

The server will respond with data like:
```
voltage: 232.3 V
current: 5.45 A
power: 1266.1 W
energy: 123.45 kWh
frequency: 49.98 Hz
```
