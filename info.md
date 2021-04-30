# AstroWeather for Home Assistant

{% if prerelease %}

## THIS IS A BETA RELEASE AND MIGHT HAVE BREAKING CHANGES IF YOU HAVE THE OLD VERSION RUNNING

---

{% endif %}

{% if version_installed.replace("v", "").replace(".","") | int < 0017  %}

## Changes as compared to your installed version:

### Changes

After the update to the actual version, you will need to open the integration options once and set the elevation of your collection.

- You now have the ability to set the elevation of your location.
- In addition to the forecast some calculations for the astronomical twilight and Moon setting, rising and phase are implemented. They indicate the darkness you can expect the upcoming night.
- Additional sensors:
  - *sensor.astroweather_elevation* - Elevation configured for this AstroWeather instance
  - *sensor.astroweather_sun_next_setting* - Next setting of the Sun, calculated for the astronomical twilight (-18°)
  - *sensor.astroweather_moon_next_rising* - Next rising of the Moon
  - *sensor.astroweather_moon_next_setting* - Nect setting of the Moon
  - *sensor.astroweather_moon_phase* - Current Moon phase in percentage

{% endif %}

{% if version_installed.replace("v", "").replace(".","") | int < 00182  %}

### Bugfixes

- Fix error when updating from previous versions caused by unknown elevation
- Fixed options flow

{% endif %}

{% if version_installed.replace("v", "").replace(".","") | int < 00183  %}

### Bugfixes

- Added missing `iot_class` to manifest.json

### Features

- Added polish language. Thanks to @nepozs

{% endif %}

---

This is a Custom Integration for [Home Assistant](https://www.home-assistant.io/). It uses the forecast data from 7Timer! to create sensor data for Home Assistant. It uses the public Machine-readable API to pull data from 7Timer!.

There is currently support for the following device types within Home Assistant:

* Sensor
* Binary Sensor

Forecast data is provided by 7Timer! on a three hourly basis.

## Installation

This Integration is part of the default HACS store.

## Configuration

The AstroWeather Integration supports the Configuration Flow of Home Assistant. There are no changes in the `configuration.yaml` required.

{% endif %}