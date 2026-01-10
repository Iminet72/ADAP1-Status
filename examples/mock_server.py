#!/usr/bin/env python3
"""Mock ADA-P1 Meter HTTP server for testing the Ada1Status integration."""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random


class MockHandler(BaseHTTPRequestHandler):
    """Handle HTTP requests and return mock sensor data."""

    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Generate realistic mock data with some variation
            data = {
                "voltage": round(230.0 + random.uniform(-5, 5), 2),
                "current": round(5.0 + random.uniform(-1, 3), 2),
                "power": round(1150.0 + random.uniform(-100, 200), 2),
                "energy": round(1234.5 + random.uniform(0, 1), 2),
                "frequency": round(50.0 + random.uniform(-0.1, 0.1), 2)
            }
            
            self.wfile.write(json.dumps(data).encode())
            print(f"Sent data: {data}")
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not found')
    
    def log_message(self, format, *args):
        """Log HTTP requests."""
        print(f"Request: {format % args}")


def main():
    """Start the mock server."""
    server_address = ('0.0.0.0', 8080)
    httpd = HTTPServer(server_address, MockHandler)
    
    print('=' * 60)
    print('Mock ADA-P1 Meter server running on port 8080')
    print('=' * 60)
    print('Available endpoints:')
    print('  GET http://localhost:8080/status')
    print('')
    print('Use this address in Home Assistant configuration:')
    print('  <your-ip>:8080')
    print('=' * 60)
    print('')
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down server...')
        httpd.shutdown()


if __name__ == '__main__':
    main()
