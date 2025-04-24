# [0.73.0](https://github.com/mawinkler/astroweather/compare/v0.72.1...v0.73.0) (2025-04-17)

### Changes

- Removed dependency to 7Timer, simplified the code.
- Added French translation. Thanks to @TallFurryMan.

# [0.72.1](https://github.com/mawinkler/astroweather/compare/v0.72.0...v0.72.1) (2025-04-14)

### Fixes

- Compatibility fix for older Home Assistant versions. Does not introduce any new functionality.

### ***Deprecation Warning***

I'm planning to remove the dependency on 7Timer, as the *experimental mode* seems to match my observations quite well. The advantage would be that I could remove a lot of complexity in the code. If you have any concerns, please let me know.

# [0.72.0](https://github.com/mawinkler/astroweather/compare/v0.71.0...v0.72.0) (2025-04-02)

### Changes

- The entities of an AstroWeather instance are now grouped into a Home Assistant device.

### Fixes

- Dependencies in pyastroweatherio and bump versions.

### ***Deprecation Warning***

I'm planning to remove the dependency on 7Timer, as the *experimental mode* seems to match my observations quite well. The advantage would be that I could remove a lot of complexity in the code. If you have any concerns, please let me know.

# [0.71.0](https://github.com/mawinkler/astroweather/compare/v0.70.2...v0.71.0) (2025-03-31)

### Changes

- Calculation of the proper icon for the current moon phase. Also requested by [#67](https://github.com/mawinkler/astroweather/issues/67).
- Calculation of the next dark night where either the moon phase is less than 5% and/or the maximum altitude during the night is less than 5° above the horizon. The limits are currently hard coded.
- About the AstroWeather Card [v0.71.0](https://github.com/mawinkler/astroweather-card/releases/tag/v0.71.0):
  - The card is now converted to TypeScript and includes all dependencies in one generated JavaScript file. This hopefully avoids outages when CDNs are not available. See [#21](https://github.com/mawinkler/astroweather-card/issues/21).
  - The graph now displays the propper units in the tooltip
  - Bumped several versions of dependent libraries, including Chart.js.

### Fixes

- Improved handling of missing data provided by weather services.

# [0.70.2](https://github.com/mawinkler/astroweather/compare/v0.70.1...v0.70.2) (2024-11-19)

### Fixes

- Moon rising and setting and UpTonight import, fixes issue [#64](https://github.com/mawinkler/astroweather/issues/64). Bump `pyastroweatherio` version to `0.70.3`

# [0.70.1](https://github.com/mawinkler/astroweather/compare/v0.70.0...v0.70.1) (2024-11-17)

### Fixes

- Bump `pyastroweatherio` version to `0.70.0`

# [0.70.0](https://github.com/mawinkler/astroweather/compare/v0.61.1...v0.70.0) (2024-11-16)

### Major changes

- Weather services provide forecast data of varying quality for different regions of the world. This makes further calculations such as ground fog, seeing etc. difficult. AstroWeather can therefore now also use data from the following services for internal calculations:
  - DWD Germany
  - Met Norway
  - NOAA U.S.
  - ECMWF
  - enventually more to come.
- This data is optionally retrieved via Open-Meteo and supplements or replaces the previous basic data. It makes sense to try out the different services and compare them with actual measured values, for example from your own weather station. This should allow you to find the best service for your area. ***I'd love to hear your feedback on this new feature and which Open-Meteo service you have chosen for your region.***
- Refactored `pyastroweatherio` from the ground up and is now using typeguard and dataframes. It was a lot of work, but it made the code much easier to read and extend, and it was fun.
- AsterWeather now requires the AstroWeather-Card in version 0.70.0+. If you get a `Entity is not a AstroWeather entity`-error clean your browser cache and reload.

### Changes

- Condition calculation now includes fog density. The fog density forecast is also included on the chart. Since fog is a very important factor in the condition calculation, AstroWeather can additionally estimate the density using temperature, relative humidity, dew point, and wind speed at ground level if you have activated the experimental mode. The condition calculation will then take into account fog forecast and the self-calculated fog density by using the worst value.
- The constellation of the Sun and Moon are now calculated.
- Additional calculations for Sun and Moon:
  - Current constallation of Sun and Moon.
  - Moon angular size, distance, relative distance and relative size, and more.

# [0.61.1](https://github.com/mawinkler/astroweather/compare/v0.61.0...v0.61.1) (2024-10-10)

### Fixes

- Hopefully fixes some install problems which occured on arm64 platforms (Yellow, RPi4) and addresses the issues [#62](https://github.com/mawinkler/astroweather/issues/62) and [#63](https://github.com/mawinkler/astroweather/issues/63). Tested platforms:
  - HassOS (arm64) 2024.10.1 - seems resolved
  - HassOS (amd64) 2024.10.1 - didn't have issues
  - Dev container (amd64) 2024.11.0.dev0 - didn't have issues
  - Non-supervised in container (amd64) 2024.10.1 - didn't have issues
- Fixes NoneType comparison [#63](https://github.com/mawinkler/astroweather/issues/63) 

# [0.61.0](https://github.com/mawinkler/astroweather/compare/v0.60.0...v0.61.0) (2024-10-05)

### Changes

- AstroWeather can now analyse the UpTonight report on comets. This makes it possible to know which comets will be in the sky tonight, their distance to the Sun and Earth and their current visual magnitude.
- One more thing with UpTonight: Check the altitude vs. time diagrams for all observable objects, bodies, and comets from the Home Assistant. See the README for examples.

# [0.60.0](https://github.com/mawinkler/astroweather/compare/v0.50.4...v0.60.0) (2024-09-13)

### Changes

- AstroWeather can now analyse the UpTonight report on solar system bodies (planets). This makes it possible to know which planets will be in the sky tonight, when they will be at their maximum elevation and in which direction they can be observed.

### Fixes

- Return ISO format datetime from get_forecasts service. Fixes [Issue 60](https://github.com/mawinkler/astroweather/issues/60).

# [0.50.4](https://github.com/mawinkler/astroweather/compare/v0.50.2...v0.50.4) (2024-07-07)

### Changes

- About the AstroWeather Card [v0.52.4](https://github.com/mawinkler/astroweather-card):
  - The card can now graph the precipitation amount.
  - The amount of precipitation for the next 6 hours, starting with astronomical darkness, is now displayed in the status description if there is precipitation.
- Forwarding setup to config entry platforms. Fixes [Issue 59](https://github.com/mawinkler/astroweather/issues/59).

# [0.50.2](https://github.com/mawinkler/astroweather/compare/v0.50.1...v0.50.2) (2024-06-05)

A lot of changes, fixes and improvements in the AstroWeather-Card are done.

### Changes

- About the AstroWeather Card [v0.52.2](https://github.com/mawinkler/astroweather-card):
  - The card can now display the precipitation forecast graphically. When activated you will get a scale on the right with up to 10mm of rainfall per hour.
  - The lifted index got a dedicated scale on the right as well.
  - The duration of astronomical darkness and deep sky darkness of the following night are now shown.
  - The tabular forecast is now filtered by the enabled subcharts and shows 7 forecast hours max.
- News on AstroWeathers condition calculation:
  - The forecast precipitation now influences the status calculation by making it worse.

### Fixes

- The icons for precipitation are now changing depending on rainfall per hour.
- Lots of fixes in the CSS section of the card.

# [0.50.1](https://github.com/mawinkler/astroweather/compare/v0.50.0...v0.50.1) (2024-05-28)

See full changelog for version 0.50.0 below.

### Fixes

- Minor fix in `pyastroweatherio` at seeing calculation.

# [0.50.0](https://github.com/mawinkler/astroweather/compare/v0.42.3...v0.50.0) (2024-05-27)

This is a massive release, at least under the hood. The pyastroweatherio library is more or less completely redeigned and much more resilient. It now offers an experimental mode which estimates atmospheric conditions like the lifted index. 

### Fixes

- AstroWeather-Card now uses new Forecast service instead of weather entity attributes. Fixes [Issue 34](https://github.com/mawinkler/astroweather/issues/34) and [Issue 50](https://github.com/mawinkler/astroweather/issues/50).
- Removed the dependency to `pytz` in `AstroWeather` and `pyastroweatherio` which introduced a blocking call.

### Breaking Changes

- Removed the sensor `seeing_plain`. This is now replaced by the sensor `seeing` giving you the calculated seeing in arcsecs.
- Removed the sensor `cloudcover_plain`. Use the sensor `cloud_cover` instead.
- Setting a name for the AstroWeather instance (see below) required to rearchitecture the entity IDs and the unique IDs. All entities of of an already existing instance will be migrated, but not the location name you defined within the AstroWeather-Card. The location name can now only be set during instance creation. If you want proper entity names, you need to delete existing instances and readd them after updating to the version 0.50 and above.

### Changes

- AstroWeather now got an experimental mode which you can activate in the integration configuration. When using this, AstroWeather is now approximately calculating the seeing, transparency, and the lifted index based on Met.no delivered data. These calculations are a challenge and still at an early stage. They need to be validated, especially for different locations. Please report back how well it works for you.
- The integration should now be much more resilient. Fixes [Issue 55](https://github.com/mawinkler/astroweather/issues/55) and [Issue 56](https://github.com/mawinkler/astroweather/issues/56).
- News on AstroWeathers condition calculation:
  - Calmness as an additional factor is now included. So the less wind the better gets the condition. Weighting can be adjusted same as seeing, transparency and the clouds.
  - You can now weaken the influence of high, medium, and low clouds. By default, all levels are equally weighted, but high clouds can be less impairing for deep sky astronomy than medium or low clouds. Depending on your typical weather, it can make sense to weaken high clouds for the calculation. Experiemt with that.
- About the AstroWeather Card:
  - Some labels on the [AstroWeather Card](https://github.com/mawinkler/astroweather-card) are shortened to avoid line breaks.
  - The card can now graph calmness and lifted index.
- Weather services used by AstroWeather:
  - Met.no now became the leading forecast service instead of 7Timer. This happened because 7Timer has repeatedly provided unreliable data or was inaccessible in the recent past.
  - In case 7Timer is not available, AstroWeather automatically falls to experimental mode.
- Replace deprecated HomeAssistantType with HomeAssistant fixes [Issue 57](https://github.com/mawinkler/astroweather/issues/57).
- You can now name the AstroWeather instances when adding them to Home Assistant. Solves [Issue 53](https://github.com/mawinkler/astroweather/issues/53).
- Completely redesigned configuration and options workflow.

# [0.42.3](https://github.com/mawinkler/astroweather/compare/v0.42.2...v0.42.3) (2024-02-09)

### Fixes

- [Issue 51](https://github.com/mawinkler/astroweather/issues/51): Added missing User-Agent header in [pyastroweatherio](https://github.com/mawinkler/pyastroweatherio).

### Changes

- Bumped versions of `aiohttp`, and `pytz` in [pyastroweatherio](https://github.com/mawinkler/pyastroweatherio).

# [0.42.2](https://github.com/mawinkler/astroweather/compare/v0.42.1...v0.42.2) (2024-01-10)

### Fixes

- Fixed deprication warning "TEMP_CELSIUS". Thanks @ChristophCaina

# [0.42.1](https://github.com/mawinkler/astroweather/compare/v0.42.0...v0.42.1) (2023-11-12)

### Fixes

- Fixed daily Deep Sky Forceast.
 
# [0.42.0](https://github.com/mawinkler/astroweather/compare/v0.31.0...v0.42.0) (2023-11-10)

### Fixes

- Fixed weired behaviour of rise and set calclations depending on the earth location.
- Fixed the Deep Sky Darkness calculation which was a tough one.
- Fixed errors at astronomical night and forecast visualization in the Lovelace card.

I spent hours on testing all the calculations for multiple geographic locations (Anchorage, Sydney, Chile, Namibia, and my location (nearby Munich)). All show a deviation of less than a couple of seconds compared to United States Naval Observatory. Please report any issues.

### Changes

- Moon set and rise time now calculated according to Naval Observatory Risings and Settings.
- Optional integration with [UpTonight](https://github.com/mawinkler/uptonight).
- Added Slovak translation. Thanks to @misa1515.
- New sensor on request: Next full Moon.
- New binary sensor for moon down during astronomical night.
- Card now displays local time for remote locations.

# [0.31.0](https://github.com/mawinkler/astroweather/compare/v0.30.0...v0.31.0) (2023-10-12)

### Changes

- Calculation of deep sky darkness.
- Calculation of astronomical night duration.
- Binary sensors for moon rising/setting or up during astronomical night.
- Updated lovelace card.

# [0.30.0](https://github.com/mawinkler/astroweather/compare/v0.23.2...v0.30.0) (2023-10-06)

### Changes

- Implemented hourly forecast.
- Changed nightly condition display.
- Card now indicates astronomical darkness graphically.
- Italien translation.
- Calculate next new Moon.
- Astronomical calculations can now be done every minute.
- Sun/Moon set and rise time is now updated after the previous one has happened.
- Beautified AstroWeather-Card Lovelace card. Card is now more customizable and able to show cloud coverage for low, medium and high clouds.

# [0.23.2](https://github.com/mawinkler/astroweather/compare/v0.23.1...v0.23.2) (2023-09-12)

### Changes

- [Issue 32](https://github.com/mawinkler/astroweather/issues/32): Implemented the new Weather forecast service for 2023.9.

# [0.23.1](https://github.com/mawinkler/astroweather/compare/v0.23.0...v0.23.1) (2023-04-26)

### Changes

- [Issue 30](https://github.com/mawinkler/astroweather/issues/30): Updated attribution to include Met.no.

# [0.23.0](https://github.com/mawinkler/astroweather/compare/v0.22.5.1...v0.23.0) (2023-04-24)

### Changes

- AstroWeather does now integrate with Met.no in addition to 7Timer. Met.no seems to deliver a more accurate cloud forecast. If enabled in the configuration the Met.no cloud forecast overrides the 7Timer cloud forecast.
- New sensors for total, high, medium and low clouds added:
  - `astroweather_clouds_area` Percentage for total cloud coverage
  - `astroweather_clouds_area_high` Percentage for high altitude cloud coverage
  - `astroweather_clouds_area_medium` Percentage for medium altitude cloud coverage
  - `astroweather_clouds_area_low` Percentage for low altitude cloud coverage

# [0.22.5.1](https://github.com/mawinkler/astroweather/compare/v0.22.5...v0.22.5.1) (2023-03-22)

### Fixes

- [Issue #27](https://github.com/mawinkler/astroweather/issues/27): Bumped pyastroweatherio to v0.22.5.3 for better handling or erroneous data.

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
