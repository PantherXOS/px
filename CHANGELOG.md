# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)

## [0.0.10]
### Fixed

- Adapted reconfiguration to default to `/etc/channels.scm`
- Update root profile packages

## [0.0.9]
### Fixed

- Update `reconfiguration` via `guix time-machine ...` approach.


## [0.0.8]
### Fixed

- Partially messed-up stout
- Fixed `px --help` to actually invoke `guix --help`

### Changed

- Updated help available at `px help`

## [0.0.7]
### Added

- Added option to run maintenance scripts: `px maintenance`

### Changed

- Subprocess commands with stderr get logged

## [0.0.6]
### Fixed

- Issue caused by missing module import in log

## [0.0.5]
### Fixed

- Issue that would prevent the application to run as non-root user

## [0.0.4]
### Fixed

- Issue where `px update apply` wouldn't actually apply all updates

### Changed

- Better logging

## [0.0.3]
### Fixed

- Missing `os` import in `px.guix`

## [0.0.2]
### Added

- Support to apply Flatpak `--user` related updates

### Fixes

- Refactored application into Flatpak and Guix class
- Properly handle missing parameters

## [0.0.1]
### Added

- Initial release
