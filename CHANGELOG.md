# Changelog

## Unreleased

### New Features

- **Staggered updates**: Each instance now refreshes at a stable offset within the update interval instead of all instances fetching at the same moment (`__init__.py`).
- **`astroweather.refresh` service**: Fetches current data and forecast right away for the targeted entities/devices, or for all instances if no target is given.
- **Manual-only mode**: A forecast interval of `0` disables automatic updates, so updates can be driven by the new service from an automation.

### Bug Fixes

- **Forecast update interval is now saved** (`config_flow.py`): `_get_config_data` read `forecast_interval` from the previously stored data instead of the submitted `user_input`, so the interval entered in the setup or options flow was silently discarded and the 5 minute default stayed in effect. It now behaves like every other field in the flow.

## [0.80.0](https://github.com/mawinkler/astroweather/compare/v0.75.0...v0.80.0) (2026-05-29)

### Improvements

- **Improved atmospheric calculations now active by default**: The improved seeing, transparency, fog density, and lifted-index calculations (previously behind the "Experimental Features" toggle) are now always active. The toggle is preserved in the UI but has no effect; a message is logged if it is still enabled. See the pyastroweatherio changelog for details.
- **Physically tuned cloud-layer weakening defaults** (`const.py`): High (cirrus) → 40, medium (altocumulus) → 70, low (stratus/fog) → 100. Previous default was 100 for all layers. Existing explicitly-configured values are unaffected.
- **Condition weight minimum raised to 1** (`config_flow.py`): The config flow no longer accepts 0 for any individual condition weight. Setting a weight to 1 is effectively negligible; setting all weights to zero caused a division-by-zero in the scoring formula.

### New Features

- **GFS Supplementary Data** Open-Meteo exposes `lifted_index`, `cape`, `boundary_layer_height`, and `visibility` only for the `gfs_seamless` model (GFS — Global Forecast System, NOAA's global numerical weather prediction model). A second, lightweight Open-Meteo request is now made in parallel with the primary model fetch — always targeting `gfs_seamless` — so these physically superior inputs are available regardless of which primary model the user has selected.
- **Binary sensor: GFS Supplementary Data** (`binary_sensor.py`, `strings.json`, `translations/`): New binary sensor that indicates whether GFS (Global Forecast System — NOAA's global numerical weather prediction model) supplementary data (boundary-layer height, lifted index, visibility, CAPE) was successfully retrieved in the last update cycle. `ON` means the improved atmospheric calculations are using real NWP model data; `OFF` means the GFS fetch failed and atmospheric conditions (seeing, fog, lifted index) are internally estimated from surface observations. The sensor is translated in all six supported languages (en, de, fr, it, pl, sk).
- **Weather entity: `gfs_supplementary_data` attribute** (`weather.py`, `const.py`): The `gfs_supplementary_data` boolean is now exposed as `ATTR_WEATHER_GFS_SUPPLEMENTARY_DATA` in the weather entity's `extra_state_attributes`, making the GFS fetch status readable from any Lovelace card or template that consumes the weather entity without requiring direct access to the binary sensor.

### Notes on methodology and accuracy

The promoted calculation variants improve the *inputs* and *mathematics* of each estimate, but all three quantities operate under fundamental constraints imposed by the data that weather APIs expose.

#### Lifted Index

**Standard path**: The Bolton (1980) approximation lifts a surface air parcel dry-adiabatically to the Lifting Condensation Level (LCL), then moist-adiabatically to 500 hPa, using only 2 m temperature, dewpoint, and sea-level pressure. The environmental temperature at 500 hPa is estimated from a fixed standard-atmosphere lapse rate — there is no actual sounding. Errors of ±3–5 °C LI are typical.

**GFS path**: Uses the `lifted_index` value computed by the GFS NWP model from its full 3-D temperature and humidity fields. This is physically far more accurate because the model has complete profile information. GFS horizontal resolution is ~13 km, which is adequate for a synoptic-scale stability indicator.

**Why it may differ from Meteoblue**: Meteoblue derives LI from ECMWF or GFS soundings too, but may apply additional post-processing, blend multiple models, or display a different vertical layer (e.g. surface-based vs. most-unstable parcel). Differences of 1–2 °C between providers are normal.

#### Seeing

**Surface-only path**: Purely empirical; estimates a seeing factor from near-surface water vapour pressure, wind speed, and relative pressure, then converts to arcseconds. Captures only the lowest few metres of the atmosphere.

**GFS path**: The planetary boundary layer (PBL) height is the primary driver (60 % weight). A shallow, stable nocturnal boundary layer (100–300 m) indicates good seeing; a deep daytime convective layer (> 1500 m) indicates poor seeing.

**Fundamental limitation — free-atmosphere turbulence is not captured**: Astronomical seeing has two independent components:

1. *Boundary-layer turbulence* (lowest 1–2 km): captured reasonably well by PBL height and surface wind. Typically contributes 0.3–0.8″ FWHM.
2. *Free-atmosphere turbulence* (2–20 km, dominated by the jet stream): contributes 0.5–1.5″ FWHM and accounts for 60–70 % of the total variance in seeing at most mid-latitude sites.

GFS does not expose upper-atmosphere turbulence metrics via the Open-Meteo API. Meteoblue's seeing forecast is based on the Antoniazzi–Giordano model, which uses wind speed and wind shear at multiple pressure levels (300, 200 hPa) extracted from ECMWF IFS — this is why Meteoblue can resolve the free-atmosphere component. A further timing effect: the GFS PBL is at its daily maximum near sunset (1500–2500 m in spring/summer), causing the seeing estimate to spike just as observations begin; the nocturnal stable boundary layer typically collapses to 100–500 m within 1–2 hours after sunset.

#### Transparency / Magnitude Degradation

**Surface-only path**: Linearly combines normalised temperature, humidity, wind, dewpoint, LI, seeing, pressure, cloud cover, and altitude with equal weights. Physically not very motivated.

**Promoted path**: Uses the Pogson relation `mag_loss = −2.5·log₁₀(transparency)` where transparency is assembled from physically motivated penalties (cloud cover 50 %, humidity haze 18 %, wind-blown aerosol 12 %, LI instability 10 %, seeing correlation 10 %).

**Fundamental limitation — aerosol and water vapour column**: Real atmospheric extinction is dominated by Rayleigh scattering (well-modelled from pressure), aerosol extinction (AOD — now partially addressed via CAMS), and precipitable water vapour (PWV — requires a humidity sounding, not just 2 m RH). Meteoblue uses CAMS aerosol forecasts and ECMWF PWV columns, which is why it can distinguish a hazy high-humidity night from a dry night with similar cloud cover.

---

## [0.75.0](https://github.com/mawinkler/astroweather/compare/v0.74.0...v0.75.0) (2026-01-13)

### Bug Fixes

- Handling of connection errors at start up.

### Changes

- Condition calculation weights are now adjustable in the range 1–100, allowing more granular tuning. Example values: Clouds 80, Fog 50, Seeing 20, Transparency 20, Calmness 50.
- Introduced improved calculation methods for seeing, magnitude degradation, lifted index, and fog density behind an "Experimental Features" toggle. These are now the default in the unreleased version above; see the pyastroweatherio changelog for details.

## [0.74.0](https://github.com/mawinkler/astroweather/compare/v0.73.0...v0.74.0) (2025-11-13)

### Bug Fixes

- AstroWeather Card v0.74.2: Highlight astronomical darkness again (background shading). Fixed `renderRoot.host`.
- AstroWeather Card v0.74.1: Fixed iOS flicker problem caused by continuous chart redraws from ResizeObserver. Improved and dampened chart redraw/update logic. Fixed the forecast table.
- AstroWeather Card v0.74.0: Fixed TypeError on undefined `action`. Fixed TypeError on null `_resolveAnimations`. Fixed graph update on card resize.
- Fix pass config entry explicitly [#73](https://github.com/mawinkler/astroweather/issues/73).
- Fix unexpected error fetching astroweather data [#72](https://github.com/mawinkler/astroweather/issues/72).

## [0.73.0](https://github.com/mawinkler/astroweather/compare/v0.72.1...v0.73.0) (2025-04-24)

### Changes

- Removed dependency to 7Timer, simplified the code.
- Added French translation. Thanks to @TallFurryMan.

## [0.72.1](https://github.com/mawinkler/astroweather/compare/v0.72.0...v0.72.1) (2025-04-14)

### Bug Fixes

- Compatibility fix for older Home Assistant versions.

## [0.72.0](https://github.com/mawinkler/astroweather/compare/v0.71.0...v0.72.0) (2025-04-02)

### Changes

- Entities of an AstroWeather instance are now grouped into a Home Assistant device.

### Bug Fixes

- Dependencies in pyastroweatherio and bump versions.

## [0.71.0](https://github.com/mawinkler/astroweather/compare/v0.70.2...v0.71.0) (2025-03-31)

### Changes

- Calculation of the proper icon for the current moon phase. Also requested by [#67](https://github.com/mawinkler/astroweather/issues/67).
- Calculation of the next dark night: moon phase < 5 % and/or maximum altitude during the night < 5° above the horizon.
- AstroWeather Card v0.71.0: Converted to TypeScript with all dependencies bundled in one JS file (avoids CDN outages, see [#21](https://github.com/mawinkler/astroweather-card/issues/21)). Graph now displays proper units in the tooltip. Bumped Chart.js and other dependencies.

### Bug Fixes

- Improved handling of missing data provided by weather services.

## [0.70.2](https://github.com/mawinkler/astroweather/compare/v0.70.1...v0.70.2) (2024-11-19)

### Bug Fixes

- Moon rising/setting and UpTonight import. Fixes [#64](https://github.com/mawinkler/astroweather/issues/64). Bumps `pyastroweatherio` to `0.70.3`.

## [0.70.1](https://github.com/mawinkler/astroweather/compare/v0.70.0...v0.70.1) (2024-11-17)

### Bug Fixes

- Bump `pyastroweatherio` to `0.70.0`.

## [0.70.0](https://github.com/mawinkler/astroweather/compare/v0.61.1...v0.70.0) (2024-11-16)

### Major Changes

- Weather services now selectable: DWD Germany, Met Norway, NOAA U.S., ECMWF, and more to come. Data is retrieved via Open-Meteo and supplements or replaces previous basic data. Try different services and compare with local measurements to find the best fit for your area.
- `pyastroweatherio` refactored from the ground up using typeguard and DataFrames.
- Requires AstroWeather Card v0.70.0+. If you see "Entity is not an AstroWeather entity", clear your browser cache and reload.

### Changes

- Condition calculation now includes fog density. AstroWeather can additionally estimate fog density from temperature, RH, dewpoint, and wind speed when experimental mode is active.
- Sun and Moon constellation calculations added.
- Moon angular size, distance, relative distance, and relative size added.

## [0.61.1](https://github.com/mawinkler/astroweather/compare/v0.61.0...v0.61.1) (2024-10-10)

### Bug Fixes

- Fixed install problems on arm64 platforms (Yellow, RPi4). Addresses [#62](https://github.com/mawinkler/astroweather/issues/62) and [#63](https://github.com/mawinkler/astroweather/issues/63).
- Fixed NoneType comparison [#63](https://github.com/mawinkler/astroweather/issues/63).

## [0.61.0](https://github.com/mawinkler/astroweather/compare/v0.60.0...v0.61.0) (2024-10-05)

### Changes

- UpTonight comet analysis: shows which comets will be in the sky tonight, their distance to the Sun and Earth, and current visual magnitude.
- UpTonight altitude vs. time diagrams accessible from Home Assistant for all observable objects, bodies, and comets.

## [0.60.0](https://github.com/mawinkler/astroweather/compare/v0.50.4...v0.60.0) (2024-09-13)

### Changes

- UpTonight solar system body analysis: shows which planets are in the sky tonight, when they reach maximum elevation, and in which direction.

### Bug Fixes

- Return ISO format datetime from `get_forecasts` service. Fixes [#60](https://github.com/mawinkler/astroweather/issues/60).

## [0.50.4](https://github.com/mawinkler/astroweather/compare/v0.50.2...v0.50.4) (2024-07-07)

### Changes

- AstroWeather Card v0.52.4: Chart now graphs precipitation amount. Precipitation for the next 6 hours from astronomical darkness is shown in the status description when non-zero.
- Forwarding setup to config entry platforms. Fixes [#59](https://github.com/mawinkler/astroweather/issues/59).

## [0.50.2](https://github.com/mawinkler/astroweather/compare/v0.50.1...v0.50.2) (2024-06-05)

### Changes

- AstroWeather Card v0.52.2: Graphical precipitation forecast with a right-hand scale up to 10 mm/h. Dedicated right-hand scale for lifted index. Duration of astronomical and deep sky darkness for the following night. Tabular forecast filtered by enabled sub-charts, capped at 7 hours.
- Forecast precipitation now influences the condition score negatively.

### Bug Fixes

- Precipitation icons now change depending on rainfall per hour.
- Numerous CSS fixes in the card.

## [0.50.1](https://github.com/mawinkler/astroweather/compare/v0.50.0...v0.50.1) (2024-05-28)

### Bug Fixes

- Minor fix in `pyastroweatherio` seeing calculation.

## [0.50.0](https://github.com/mawinkler/astroweather/compare/v0.42.3...v0.50.0) (2024-05-27)

### Breaking Changes

- Removed sensor `seeing_plain`; replaced by `seeing` reporting calculated seeing in arcseconds.
- Removed sensor `cloudcover_plain`; use `cloud_cover` instead.
- Entity IDs and unique IDs rearchitected due to named instances. Existing entities migrate automatically; the location name configured in the card does not. Delete and re-add existing instances for clean entity names.

### Changes

- Experimental mode: AstroWeather now estimates seeing, transparency, and lifted index from Met.no data. Activate in the integration configuration.
- Calmness added as a condition factor. Wind weighting is configurable alongside clouds, seeing, and transparency.
- Configurable per-layer cloud weakening: high clouds can be set to have less impact than medium/low clouds.
- AstroWeather Card: shortened labels to avoid line breaks; added calmness and lifted index graphs.
- Met.no is now the primary forecast service (7Timer demoted to fallback due to reliability issues).
- Named AstroWeather instances. Solves [#53](https://github.com/mawinkler/astroweather/issues/53).
- Completely redesigned configuration and options workflow.
- Replace deprecated `HomeAssistantType` with `HomeAssistant`. Fixes [#57](https://github.com/mawinkler/astroweather/issues/57).

### Bug Fixes

- AstroWeather Card now uses new Forecast service instead of weather entity attributes. Fixes [#34](https://github.com/mawinkler/astroweather/issues/34) and [#50](https://github.com/mawinkler/astroweather/issues/50).
- Removed dependency on `pytz`, which introduced a blocking call.

## [0.42.3](https://github.com/mawinkler/astroweather/compare/v0.42.2...v0.42.3) (2024-02-09)

### Bug Fixes

- [#51](https://github.com/mawinkler/astroweather/issues/51): Added missing User-Agent header in pyastroweatherio.
- Bumped `aiohttp` and `pytz` in pyastroweatherio.

## [0.42.2](https://github.com/mawinkler/astroweather/compare/v0.42.1...v0.42.2) (2024-01-10)

### Bug Fixes

- Fixed deprecation warning `TEMP_CELSIUS`. Thanks @ChristophCaina.

## [0.42.1](https://github.com/mawinkler/astroweather/compare/v0.42.0...v0.42.1) (2023-11-12)

### Bug Fixes

- Fixed daily Deep Sky Forecast.

## [0.42.0](https://github.com/mawinkler/astroweather/compare/v0.31.0...v0.42.0) (2023-11-10)

### Changes

- Moon set and rise calculated according to Naval Observatory Risings and Settings.
- Optional integration with [UpTonight](https://github.com/mawinkler/uptonight).
- Added Slovak translation. Thanks to @misa1515.
- New sensor: next full Moon.
- New binary sensor: moon down during astronomical night.
- Card now displays local time for remote locations.

### Bug Fixes

- Fixed rise/set calculations for different geographic locations.
- Fixed Deep Sky Darkness calculation.
- Fixed errors at astronomical night and forecast visualisation in the card.

## [0.31.0](https://github.com/mawinkler/astroweather/compare/v0.30.0...v0.31.0) (2023-10-12)

### Changes

- Deep sky darkness calculation.
- Astronomical night duration calculation.
- Binary sensors for moon rising/setting/up during astronomical night.
- Updated Lovelace card.

## [0.30.0](https://github.com/mawinkler/astroweather/compare/v0.23.2...v0.30.0) (2023-10-06)

### Changes

- Hourly forecast implemented.
- Changed nightly condition display.
- Card now indicates astronomical darkness graphically.
- Italian translation added.
- Next new Moon calculation.
- Astronomical calculations can now run every minute.
- Sun/Moon set and rise time updated after the previous event has passed.
- Card more customisable; shows cloud coverage for low, medium, and high clouds separately.

## [0.23.2](https://github.com/mawinkler/astroweather/compare/v0.23.1...v0.23.2) (2023-09-12)

### Changes

- [#32](https://github.com/mawinkler/astroweather/issues/32): Implemented the new Weather forecast service for HA 2023.9.

## [0.23.1](https://github.com/mawinkler/astroweather/compare/v0.23.0...v0.23.1) (2023-04-26)

### Changes

- [#30](https://github.com/mawinkler/astroweather/issues/30): Updated attribution to include Met.no.

## [0.23.0](https://github.com/mawinkler/astroweather/compare/v0.22.5.1...v0.23.0) (2023-04-24)

### Changes

- Met.no integration added alongside 7Timer. Met.no delivers a more accurate cloud forecast; when enabled it overrides the 7Timer cloud forecast.
- New sensors for total, high, medium, and low cloud coverage: `astroweather_clouds_area`, `astroweather_clouds_area_high`, `astroweather_clouds_area_medium`, `astroweather_clouds_area_low`.

## [0.22.5.1](https://github.com/mawinkler/astroweather/compare/v0.22.5...v0.22.5.1) (2023-03-22)

### Bug Fixes

- [#27](https://github.com/mawinkler/astroweather/issues/27): Bumped pyastroweatherio to v0.22.5.3 for better handling of erroneous data.

## [0.22.5](https://github.com/mawinkler/astroweather/compare/v0.22.4...v0.22.5) (2023-02-09)

### Bug Fixes

- [#25](https://github.com/mawinkler/astroweather/issues/25): Fixed sensor units for string values.

## [0.22.4](https://github.com/mawinkler/astroweather/compare/v0.22.3...v0.22.4) (2023-01-15)

### Bug Fixes

- [#21](https://github.com/mawinkler/astroweather/issues/21): Replaced deprecated `DEVICE_CLASS_*` constants with `SensorDeviceClass` enums (deprecated since HA Core 2021.12).

## [0.22.3](https://github.com/mawinkler/astroweather/compare/v0.22.2...v0.22.3) (2022-10-29)

### Bug Fixes

- [#19](https://github.com/mawinkler/astroweather/issues/19): Replaced deprecated `IMPERIAL_SYSTEM` and `is_metric`/`name` properties with instance checks (deprecated since HA Core 2022.11).

## [0.22.2](https://github.com/mawinkler/astroweather/compare/v0.22.1...v0.22.2) (2022-07-22)

### Bug Fixes

- [#18](https://github.com/mawinkler/astroweather/issues/18): Implemented `native_value` and `native_unit_of_measurement` for temperature conversions.

## [0.22.1](https://github.com/mawinkler/astroweather/compare/v0.22.0...v0.22.1) (2022-07-20)

### Breaking Changes

- Config flow now requires an additional timezone entry. Delete and re-add the integration via Devices & Services when upgrading from any previous version.

### Changes

- Timezone calculated from the configured timezone entry, enabling multiple instances with different time zones.

### Bug Fixes

- [#16](https://github.com/mawinkler/astroweather/issues/16) and [#17](https://github.com/mawinkler/astroweather/issues/17): Removed `timezonefinder` / `py-h3` dependency which failed to compile on some HA deployments (e.g. HassOS on RPi).

## [0.22.0](https://github.com/mawinkler/astroweather/compare/v0.21.0...v0.22.0) (2022-07-10)

### Changes

- Timezone calculated from configured geographic location, enabling multiple instances with different time zones.
- Added nautical dusk (−12°), dew point (Magnus-Tetens), sun altitude/azimuth, and moon altitude/azimuth calculations.

### Bug Fixes

- Civil sunset/sunrise now correctly calculated for −6° (dusk).
- [#15](https://github.com/mawinkler/astroweather/issues/15): `native_temperature`, `native_temperature_unit`, `native_wind_speed`.
- [#16](https://github.com/mawinkler/astroweather/issues/16): Added missing weather types (`tsday`, `tsnight`, `tsrainday`, `tsrainnight`).

## [0.21.0](https://github.com/mawinkler/astroweather/compare/v0.20.9...v0.21.0) (2022-05-13)

### Bug Fixes

- Sunset/sunrise calculations for polar regions now supported. Fixes [#13](https://github.com/mawinkler/astroweather/issues/13). Thanks @samhaa.

## [0.20.9](https://github.com/mawinkler/astroweather/compare/v0.20.8...v0.20.9) (2022-04-08)

### Changes

- Condition calculation weights now configurable. Default: clouds ×3, seeing ×2, transparency ×1.
- Reintroduced cloud coverage sensor alongside cloudless sensor.
- Added forecast length sensor (available forecast hours).
- Day names instead of "Today"/"Tomorrow" for the nightly forecast.
- Updated German and Polish translations.

### Bug Fixes

- `strings.json` fixes.

## [0.20.8](https://github.com/mawinkler/astroweather/compare/v0.20.7...v0.20.8) (2022-03-14)

### Changes

- Improved resilience against incomplete data.

## [0.20.7](https://github.com/mawinkler/astroweather/compare/v0.20.6...v0.20.7) (2022-03-10)

### Changes

- Moon phase added as a weather entity attribute.
- API query precision to 7Timer reduced to two decimal digits to protect location privacy.
- Forecast polling interval changed to 30 min – 4 h range (default 1 h) to reduce load on 7Timer.

## [0.20.6](https://github.com/mawinkler/astroweather/compare/v0.20.5...v0.20.6) (2022-02-22)

### Bug Fixes

- Corrected unit for lifted index (LI).

## [0.20.5](https://github.com/mawinkler/astroweather/compare/v0.20.4...v0.20.5) (2022-02-22)

### Bug Fixes

- Proper handling of timestamps.

## [0.20.4](https://github.com/mawinkler/astroweather/compare/v0.20.1...v0.20.4) (2022-02-19)

### Changes

- New icons for moon rising and setting.
- Added sensor `astroweather_10m_wind_speed_plain`.

### Bug Fixes

- Wind speed now showing in m/s.

## [0.20.1](https://github.com/mawinkler/astroweather/compare/v0.20.0...v0.20.1) (2022-02-16)

### Bug Fixes

- Timestamps not showing correctly on the companion app.
- `sun_next_rising` attribute was returning the `sun_next_setting` value.

## [0.20.0](https://github.com/mawinkler/astroweather/compare/v0.0.18.3...v0.20.0) (2022-02-15)

### Breaking Changes

- Replaced sensors: `view_conditions` → `condition`, `forecast0` → `deepsky_forecast_today`, `forecast0_plain` → `deepsky_forecast_today_plain`, `forecast1` → `deepsky_forecast_tomorrow`, `forecast0_plain` → `deepsky_forecast_tomorrow_plain`, `sun_next_setting` → `sun_next_rising_astronomical`.
- Removed `view_conditions_plain`.

### New Features

- Home Assistant weather entity added.
- Optional [AstroWeather Card](https://github.com/mawinkler/astroweather-card) for Lovelace.
- New sensors: `deepsky_forecast_today_desc`, `deepsky_forecast_tomorrow_desc`, `sun_next_setting_astronomical`, `sun_next_rising_astronomical`, `sun_next_setting`, `sun_next_rising`.
- Condition, clouds, seeing, and transparency sensors now report as percentage (higher = better).
