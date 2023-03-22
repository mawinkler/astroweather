# [0.22.5.1](https://github.com/mawinkler/astroweather/compare/v0.22.5...v0.22.5.1) (2023-03-22)

### Fixes

- [Issue #25](https://github.com/mawinkler/astroweather/issues/27): Bumped pyastroweatherio to v0.22.5.3 for better handling or erroneous data.

# [0.22.5](https://github.com/mawinkler/astroweather/compare/v0.22.4...v0.22.5) (2023-02-09)

### Fixes

- [Issue #25](https://github.com/mawinkler/astroweather/issues/25): Fixed sensor units for string values.

# [0.22.4](https://github.com/mawinkler/astroweather/compare/v0.22.3...v0.22.4) (2023-01-15)

### Fixes

- [Issue #21](https://github.com/mawinkler/astroweather/issues/21): Changed `DEVICE_CLASS_*` to SensorDeviceClass enums. The `DEVICE_CLASS_*` constants have been deprecated and replaced in Home Assistant Core 2021.12.

# [0.22.3](https://github.com/mawinkler/astroweather/compare/v0.22.2...v0.22.3) (2022-10-29)

### Fixes

- [Issue #19](https://github.com/mawinkler/astroweather/issues/19): As of Home Assistant Core 2022.11, the IMPERIAL_SYSTEM is deprecated, replaced by US_CUSTOMARY_SYSTEM. The is_metric and name properties of a unit system are likewise deprecated and should not be used. Adjusted to use instance check instead.

# [0.22.2](https://github.com/mawinkler/astroweather/compare/v0.22.1...v0.22.2) (2022-07-22)

### Fixes

- [Issue #18](https://github.com/mawinkler/astroweather/issues/18): Temperature conversions with `native_value` and `native_unit_of_measurement` are now implemented in the sensor entity [Reference](https://developers.home-assistant.io/blog/2021/08/12/sensor_temperature_conversion/).

# [0.22.1](https://github.com/mawinkler/astroweather/compare/v0.22.0...v0.22.1) (2022-07-20)

### Changes

- Calculate the timezone of the AstroWeather instance based on configured timezone. This makes it possible to configure multiple instances of AstroWeather for different locations with potentially different time zones.

### Fixes

- [Issue #16](https://github.com/mawinkler/astroweather/issues/16) and [Issue #17](https://github.com/mawinkler/astroweather/issues/17): The introduction of the module [timezonefinder](https://github.com/jannikmi/timezonefinder) with it's nested dependency to [py-h3](https://github.com/uber/h3-py) failed while compiling the `c`-module h3 on some home assistant deployment variants (e.g. Home Assistant Operating System on RPi). The config flow now allows to select the timezone for the specific AstroWeather instance for which reason the dependency to `timezonefinder` is not required anymore.

### Breaking Changes

- The config flow now requires an additional config entry. To upgrade from any previous version please delete the integration and add it again via the `Devices & Services` section of your Home Assistant

# [0.22.0](https://github.com/mawinkler/astroweather/compare/v0.21.0...v0.22.0) (2022-07-10)

### Changes

- Calculate the timezone of the AstroWeather instance based on configured geographical location for the instance. This makes it possible to configure multiple instances of AstroWeather for different locations with potentially different time zones. Previously the timezone of the os was used.
- Added nautical dusk calculated for -12 degrees
- Added dew point calculation based on the Magnus-Tetens formula
- Added sun altitude and azimuth calculations
- Added moon altitude and azimuth calculations

### Fixes

- Calculations for civil sunset and sunrise are now calculated for -6 degrees (dusk)
- [Issue #15](https://github.com/mawinkler/astroweather/issues/15): Properties `native_temperature`, `native_temperature_unit`, `native_wind_speed`
- [Issue #16](https://github.com/mawinkler/astroweather/issues/16): Added some missing weather types in `pyastroweatherio` (`tsday`, `tsnight`, `tsrainday`, `tsrainnight`)

# [0.21.0](https://github.com/mawinkler/astroweather/compare/v0.20.9...v0.21.0) (2022-05-13)

### Fixes

- Calculations for sunset and sunrise in polar regions are now supported. Thank you for @samhaa reporting [this](https://github.com/mawinkler/astroweather/issues/13).

# [0.20.9](https://github.com/mawinkler/astroweather/compare/v0.20.8...v0.20.9) (2022-04-08)

### Changes

- The weightings for the condition calculation is now configurable and can be adapted to your needs. Default isto weight clouds three times, seeing twice and transparency once.
- Reintroduced cloud coverage sensor alongside cloudless sensor
- Added forecast length sensor giving the available time period of forecast data in hours
- Day names instead of `Today` and `Tomorrow` for the nightly forecast
- Updated German and Polish translations

### Fixes

- `strings.json`

# [0.20.8](https://github.com/mawinkler/astroweather/compare/v0.20.7...v0.20.8) (2022-03-14)

### Changes

- Improved resilience against incomplete data.

# [0.20.7](https://github.com/mawinkler/astroweather/compare/v0.20.6...v0.20.7) (2022-03-10)

### Changes

- Added the moon phase as an attribute for the weather component.
- Changed the maximum precision for the API query to 7Timer to two digits to protect your privacy.
- Changed the forecast polling interval to be in a range of 30 mins to 4 hours with a default of 1h.

> Note: The change about the forecast polling interval was required since AstroWeather is becoming more popular and has started to overwhelm the 7Timer service. The integration was already consuming about 20% of its capacity. The forecast quality will not downgrade since the service is updating its data on a six-hourly basis.

# [0.20.6](https://github.com/mawinkler/astroweather/compare/v0.20.5...v0.20.6) (2022-02-22)

### Fixes

- Corrected unit for lifted index (LI)

# [0.20.5](https://github.com/mawinkler/astroweather/compare/v0.20.4...v0.20.5) (2022-02-22)

### Fixes

- Proper handling of timestamps

# [0.20.4](https://github.com/mawinkler/astroweather/compare/v0.20.1...v0.20.4) (2022-02-19)

### Fixes

- Wind speed now showing in m/s

### Changes

- New icons for moon rising and setting
- Added sensor astroweatherq_10m_wind_speed_plain

# [0.20.1](https://github.com/mawinkler/astroweather/compare/v0.20.0...v0.20.1) (2022-02-16)

### Fixes

- Timestamps not showing correctly on the companion app
- The sun_next_rising attribute was actually showing the sun_next_setting value

# [0.20.0](https://github.com/mawinkler/astroweather/compare/v0.0.18.3...v0.20.0) (2022-02-15)

### Features

- Added a Home Assistant weather entity
- Added support for an optional [weather card](https://github.com/mawinkler/astroweather-card) for Lovelace
- Bump to version 0.20.0
- New sensors:
  - `deepsky_forecast_today_desc` Deepsky forecast today description
  - `deepsky_forecast_tomorrow_desc` Deepsky forecast tomorrow description
  - `sun_next_setting_astronomical` Sun next setting astronomical twilight
  - `sun_next_rising_astronomical` Sun next rising astronomical twilight
  - `sun_next_setting` Sun next setting civil twilight
  - `sun_next_rising` Sun next rising civil twilight
- Changed sensors now reporting as percentage (the higher the percentage, the better for sky observations):
  - `condition`
  - `clouds`
  - `seeing`
  - `transparency`

### Breaking Changes

- The following sensors got replaced:
  - `view_conditions` with `condition`
  - `forecast0` with `deepsky_forecast_today`
  - `forecast0_plain` with `deepsky_forecast_today_plain`
  - `forecast1` with `deepsky_forecast_tomorrow`
  - `forecast0_plain` with `deepsky_forecast_tomorrow_plain`
  - `sun_next_setting` with `sun_next_rising_astronomical`
- The following sensors got removed:
  - `view_conditions_plain`
