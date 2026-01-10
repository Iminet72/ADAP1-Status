# Example configuration for testing the integration

This directory contains example files for testing the Ada1Status integration.

## Testing the Integration

Since the integration connects to a real ADA-P1 Meter device, you can test it by:

1. Setting up a mock HTTP server that returns the expected JSON format
2. Configuring the integration to point to your test server

### Mock Server Example

You can create a simple mock server using Python:

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class MockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            data = {
                "voltage": 230.5,
                "current": 5.2,
                "power": 1198.6,
                "energy": 1234.5,
                "frequency": 50.0
            }
            
            self.wfile.write(json.dumps(data).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress logging

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8080), MockHandler)
    print('Mock ADA-P1 Meter server running on port 8080...')
    server.serve_forever()
```

Save this as `mock_server.py` and run it with:
```bash
python3 mock_server.py
```

Then configure the integration in Home Assistant to connect to `<your-ip>:8080`.
