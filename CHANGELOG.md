# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- Decode every button press on Linux/BlueZ hosts. BlueZ merges the service
  UUIDs of all advertisements from the shared address into one cached list,
  so previously only the first press after a cache reset was decoded.

## [1.0.0] - 2025-06-08

### Added
- Initial release