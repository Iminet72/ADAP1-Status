# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-10

### Added
- Initial release of Ada1Status integration
- Config flow for easy setup via Home Assistant UI
- Support for 5 sensor types:
  - Voltage (V)
  - Current (A)
  - Power (W)
  - Energy (kWh)
  - Frequency (Hz)
- HTTP polling from ADA-P1 Meter device
- Configurable update interval (default: 30 seconds)
- English and Hungarian translations
- Proper device classes and state classes for sensors
- Automatic URL validation during setup
- Error handling for connection issues
