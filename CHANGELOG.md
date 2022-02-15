# [0.20.0](https://github.com/mawinkler/astroweather/compare/v0.20.0...v0.0.18.3) (2022-02-15)

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
