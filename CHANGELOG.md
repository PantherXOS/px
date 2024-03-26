# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)

## [0.0.20]

### Changed

- Ugly work-around to handle recent changes in guix, and allow recovering from it https://issues.guix.gnu.org/49610

## [0.0.19]

### Fixed

- Properly handle desktop files in org format (e.g. `org.keepassxc.KeePassXC.desktop`)

## [0.0.18]

### Changed

- Removed `--disable-authentication` from all commands (so channels are authenticated now)

## [0.0.16]

### Added

- Shortcut to reconfigre with `px reconfigure`

## [0.0.15]

### Added

- Support for handling ARM u-boot, firmware and overlays for Raspberry Pi

## [0.0.14]

### Fixed

- License

## [0.0.13]

### Fixed

- Updated text to reflect new channels file location.

### Changed

- Running `px` shows the help text
- Updated help text with info on how-to search for services

## [0.0.12]

### Changed

- Default channels file moved to `/etc/guix/channels.scm`

## [0.0.11]

### Changed

- Cleanup, added license

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
