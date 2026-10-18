# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2026-10-18

### Added
- Event entities: one per button (6 for the R5, 3 for the S-Mate) with the
  event types `short`, `double` and `long`. They show up as targets in the
  automation editor, keep a history of presses and can be used on
  dashboards. Device triggers and the `sonoff_ble_event` event still work.
- Unloading/reloading the integration.

### Fixed
- Decode every button press on Linux/BlueZ hosts. BlueZ merges the service
  UUIDs of all advertisements from the shared address into one cached list,
  so previously only the first press after a cache reset was decoded.

## [1.0.0] - 2025-06-08

### Added
- Initial release