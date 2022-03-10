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
