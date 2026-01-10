#!/usr/bin/env python3
"""
Simple HTTP server to simulate ADA-P1 Meter responses.
Use this for testing the Ada1Status integration without a real device.

Usage:
    python3 examples/mock_server.py

Then configure the integration with host: localhost, port: 8989
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random
import time


class MockADAP1Handler(BaseHTTPRequestHandler):
    """Handler for simulating ADA-P1 Meter HTTP responses."""

    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/status":
            # Generate mock JSON data
            uptime_sec = int(time.time() % 100000)
            uptime_hours = uptime_sec // 3600
            uptime_mins = (uptime_sec % 3600) // 60
            
            data = {
                "os_version": "1.2.3",
                "local_ip": "192.168.1.100",
                "hostname": "ada-p1-meter",
                "ssid": "MockWiFi",
                "mqtt_server": "192.168.1.10",
                "mqtt_connected": random.choice([True, False]),
                "uptime_hhmm": f"{uptime_hours:02d}:{uptime_mins:02d}",
                "uptime_seconds": uptime_sec,
                "wifi_rssi": -60 + random.randint(-10, 10),
                "wifi_channel": random.choice([1, 6, 11]),
                "serial_recent_sec": random.randint(0, 30),
                "heap_total": 327680,
                "heap_free": 123456 + random.randint(-10000, 10000),
                "heap_min_free": 100000,
                "heap_max_alloc": 98304,
                "heap_fragmentation": random.randint(10, 25),
                "fs_total": 1048576,
                "fs_used": 524288 + random.randint(-50000, 50000),
                "watchdog_enabled": True,
                "watchdog_last_kick_ms": random.randint(50, 200),
                "telegram_url_mode": False,
                "telegram_url_set": True,
                "rules_loaded": True,
                "chip_cores": 2,
                "ack_items": random.randint(0, 5),
            }
            
            # Send JSON response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data, indent=2).encode())
        else:
            # Return 404 for other paths
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Not Found. Use /status endpoint.")

    def log_message(self, format, *args):
        """Log requests."""
        print(f"[{self.log_date_time_string()}] {format % args}")


def run_server(port=8989):
    """Run the mock server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, MockADAP1Handler)
    print(f"Mock ADA-P1 Meter server running on http://localhost:{port}")
    print(f"JSON status endpoint: http://localhost:{port}/status")
    print("Configure Home Assistant integration with:")
    print(f"  Host: localhost")
    print(f"  Port: {port}")
    print("Press Ctrl+C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()


if __name__ == '__main__':
    run_server()
