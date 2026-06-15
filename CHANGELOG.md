# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-06-15

### Fixed
- **Device duplication on Home Assistant restarts** – device and entity
  identifiers are now derived from the stable `config_entry.entry_id` instead
  of `CONF_HOST`.  Using the network address as an identifier caused duplicate
  devices to appear whenever the host string differed even slightly (e.g. IP
  vs. hostname, leading/trailing whitespace, DHCP address change).
- Config-flow unique-ID is now derived from the normalised (lower-cased,
  stripped) host value, preventing accidental double-entries for the same
  physical device.

### Changed
- Config entry schema bumped to **version 2**.  A migration step
  (`async_migrate_entry`) automatically updates the device and entity
  registry entries of existing installations so that no manual
  re-configuration is required.

## [1.0.0] - 2026-01-10

### Added
- Initial release of Adap1Status integration
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
