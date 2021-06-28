# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.4.0] - 2021-06-28
### Added
- VTEC for K-Pro v2/3/4 and S300 v3
- FANC for S300 v3

### Changed
- Fix SCS for S300 v3

## [3.3.0] - 2021-06-16
### Added
- Analog inputs for S300 v3

## [3.2.0] - 2021-03-23
### Changed
- Fixed specific pressure and temperature sensor formulas breaking the app when selected

### Added
- If setup file is found empty, default setup would be loaded

## [3.1.0] - 2021-01-10
### Changed
- Fix for ecu connection after setup changes

### Added
- Custom linear ecu analog inputs 

## [3.0.0] - 2020-12-17
### Changed
- Fix for Chromium update pop-up

### Added
- Hondata S300 v3 compatibility

## [2.6.0] - 2020-11-03
### Changed
- Corrected MR2 W30 fuel tank formula
- Odometer has been revised to be more precise and no reboot needed after changes

### Added
- Integra DC5 fuel tank formula
- Accord CL9 fuel tank formula
- 30 psi fluid pressure transducer formula

## [2.5.0] - 2020-05-27
### Changed
- Fixed bug with odometer units (thanks @acolonnh)
- Removed neutral from gear indicator since K-pro is not able to sense neutral
- More colorful RPM bar by default

### Added
- Possibility to upload the configuration from previous versions (from 2.3.2 and on) so no need to reconfigure everything again
- Color sectors now allow decimal point ranges

## [2.4.0] - 2020-03-22
### Changed
- Fronted more adaptative to other screen resolutions (Bootstrap 4)
- Fixed bug in setup with formulas
- Simplified setup (deleted scs, fan, mil, gear and time configurations)

## [2.3.2] - 2020-02-01
### Changed
- Bugfix for analogs inputs in K-Pro V3
- Revised USB connection
- Changed default tps range to 20-30% for day/night mode

## [2.3.1] - 2020-01-09
### Added
- MR2 W20 fuel tank formula

### Changed
- No reboot needed after saving a new setup

## [2.3.0] - 2019-12-03
### Added
- Day and night color modes

### Changed
- Fixed K-pro v2/v3 firmware version value
- Fixed ect and iat temperature values
- Restricted analog inputs units depending on chosen formula

## [2.2.0] - 2019-10-26
### Added
- Reset configuration feature
- SCS (Service Connector) status displayed
- K-Pro firmware version displayed 

### Changed
- Smaller SD card image

## [2.1.2] - 2019-09-19
### Added
- Civic EK fuel tank formula

### Changed
- Fixed not available used tags in setup dropdowns

## [2.1.1] - 2019-06-19
### Added
- Version number showed also in the actual dashboard
- New dashboard template system

### Changed
- Fixed connection with Kpro after last firmware from Kmanager V4.4.1

## [2.1.0] - 2019-04-11
### Added
- Screen rotation option

## [2.0.0] - 2019-01-24
### Added
- New version base 
