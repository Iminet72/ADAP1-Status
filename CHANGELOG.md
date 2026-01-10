# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-10

### Added
- Initial release of Ada1Status Home Assistant integration
- Support for ADA-P1 Meter device monitoring via HTTP
- Configuration flow for easy setup through UI
- Multiple sensor types:
  - Voltage sensor (V)
  - Current sensor (A)
  - Power sensor (W)
  - Energy sensor (kWh)
  - Frequency sensor (Hz)
- Multi-language support (English, Hungarian)
- HACS compatibility
- Mock server for testing
- Comprehensive documentation

### Features
- Automatic device polling every 30 seconds
- Device information tracking
- Energy sensor with state class for long-term statistics
- Proper device classes for all sensors

[1.0.0]: https://github.com/Iminet72/adaP1Status/releases/tag/v1.0.0
