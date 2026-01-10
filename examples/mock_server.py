#!/usr/bin/env python3
"""
Simple HTTP server to simulate ADA-P1 Meter responses.
Use this for testing the Ada1Status integration without a real device.

Usage:
    python3 examples/mock_server.py

Then configure the integration with: http://localhost:8080
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import random
import time


class MockADAP1Handler(BaseHTTPRequestHandler):
    """Handler for simulating ADA-P1 Meter HTTP responses."""

    def do_GET(self):
        """Handle GET requests."""
        # Generate mock data with some variation
        voltage = 230.0 + random.uniform(-5, 5)
        current = 5.0 + random.uniform(-1, 1)
        power = voltage * current
        # Energy increases over time
        energy = 100.0 + (time.time() % 1000) / 10
        frequency = 50.0 + random.uniform(-0.1, 0.1)

        # Format response
        response = f"""voltage: {voltage:.1f} V
current: {current:.2f} A
power: {power:.1f} W
energy: {energy:.2f} kWh
frequency: {frequency:.2f} Hz
"""

        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response.encode())

    def log_message(self, format, *args):
        """Log requests."""
        print(f"[{self.log_date_time_string()}] {format % args}")


def run_server(port=8080):
    """Run the mock server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, MockADAP1Handler)
    print(f"Mock ADA-P1 Meter server running on http://localhost:{port}")
    print("Configure Home Assistant integration with: http://localhost:8080")
    print("Press Ctrl+C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()


if __name__ == '__main__':
    run_server()
