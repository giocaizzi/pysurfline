from datetime import datetime
import pandas as pd
import pytest

from pysurfline.models import (
    Time,
    Weather,
    Wind,
    Surf,
    Swell,
    TideLocation,
    Tide,
    SunriseSunsetTime,
    Forecast,
    SpotForecasts,
)

TIMESTAMP = 1629475200
DATETIME = datetime(2021, 8, 20, 16, 0)
WEATHER_TEMP = 20.0
WEATHER_TEMP = "Sunny"
WIND_SPEED = 10.0
WIND_DIRECTION = 180.0
SURF_MIN = 1.0
SURF_MAX = 2.0
SWELL_HEIGHT = 1.0
SWELL_DIRECTION = 180.0
SWELL_DIRECTION_MIN = 170.0
SWELL_PERIOD = 10.0
FORECASTLOCATION_NAME = "Test"
FORECASTLOCATION_MIN = 1.0
FORECASTLOCATION_MAX = 2.0
FORECASTLOCATION_LON = 10.0
FORECASTLOCATION_LAT = 20.0
FORECASTLOCATION_MEAN = 1.5
TIDE_TYPE = "High"
TIDE_HEIGHT = 1.0

FORECAST = {
    "timestamp": TIMESTAMP,
    "weather": {"temperature": WEATHER_TEMP, "condition": WEATHER_TEMP},
    "wind": {"speed": WIND_SPEED, "direction": WIND_DIRECTION},
    "surf": {"min": SURF_MIN, "max": SURF_MAX},
    # it's a list of swells
    "swells": [
        {
            "height": SWELL_HEIGHT,
            "direction": SWELL_DIRECTION,
            "directionMin": SWELL_DIRECTION_MIN,
            "period": SWELL_PERIOD,
        }
    ],
}

TIDE = {
    "timestamp": TIMESTAMP,
    "type": TIDE_TYPE,
    "height": TIDE_HEIGHT,
}

SUNRISESUNSETTIME = {
    "midnight": TIMESTAMP,
    "sunrise": TIMESTAMP,
    "sunset": TIMESTAMP,
}

TIDELOCATION = {
    "name": FORECASTLOCATION_NAME,
    "min": FORECASTLOCATION_MIN,
    "max": FORECASTLOCATION_MAX,
    "lon": FORECASTLOCATION_LON,
    "lat": FORECASTLOCATION_LAT,
    "mean": FORECASTLOCATION_MEAN,
}

SUNRISESUNSETTIMES = [
    SUNRISESUNSETTIME,
    SUNRISESUNSETTIME,
    SUNRISESUNSETTIME,
]

FORECASTS = [
    FORECAST,
    FORECAST,
    FORECAST,
]

TIDES = [
    TIDE,
    TIDE,
    TIDE,
]


def test_Time():
    t = Time(TIMESTAMP)
    assert t.timestamp == TIMESTAMP
    assert isinstance(t.dt, datetime)
    assert t.dt == DATETIME


def test_Weather():
    w = Weather(WEATHER_TEMP, WEATHER_TEMP)
    assert w.temperature == WEATHER_TEMP
    assert w.condition == WEATHER_TEMP


def test_Wind():
    w = Wind(WIND_SPEED, WIND_DIRECTION)
    assert w.speed == WIND_SPEED
    assert w.direction == WIND_DIRECTION


def test_Surf():
    s = Surf(SURF_MIN, SURF_MAX)
    assert s.min == SURF_MIN
    assert s.max == SURF_MAX


def test_Swell():
    s = Swell(SWELL_HEIGHT, SWELL_DIRECTION, SWELL_DIRECTION_MIN, SWELL_PERIOD)
    assert s.height == SWELL_HEIGHT
    assert s.direction == SWELL_DIRECTION
    assert s.directionMin == SWELL_DIRECTION_MIN
    assert s.period == SWELL_PERIOD


def test_ForecastLocation():
    f = TideLocation(
        FORECASTLOCATION_NAME,
        FORECASTLOCATION_MIN,
        FORECASTLOCATION_MAX,
        FORECASTLOCATION_LON,
        FORECASTLOCATION_LAT,
        FORECASTLOCATION_MEAN,
    )
    assert f.name == FORECASTLOCATION_NAME
    assert f.min == FORECASTLOCATION_MIN
    assert f.max == FORECASTLOCATION_MAX
    assert f.lon == FORECASTLOCATION_LON
    assert f.lat == FORECASTLOCATION_LAT
    assert f.mean == FORECASTLOCATION_MEAN


def test_tide():
    t = Tide(TIMESTAMP, TIDE_TYPE, TIDE_HEIGHT)
    assert t.timestamp.dt == DATETIME
    assert t.type == TIDE_TYPE
    assert t.height == TIDE_HEIGHT


def test_SunriseSunsetTime():
    d = SunriseSunsetTime(TIMESTAMP, TIMESTAMP, TIMESTAMP)
    assert isinstance(d.midnight, Time)
    assert isinstance(d.sunrise, Time)
    assert isinstance(d.sunset, Time)


def test_ForecastObject():
    f = Forecast(**FORECAST)
    assert isinstance(f.timestamp, Time)
    assert isinstance(f.weather, Weather)
    assert isinstance(f.wind, Wind)
    assert isinstance(f.surf, Surf)
    assert isinstance(f.swells, list)
    assert isinstance(f.swells[0], Swell)


def test_SpotForecast():
    s = SpotForecasts(
        "TestID", "Test", FORECASTS, SUNRISESUNSETTIMES, TIDES, TIDELOCATION,
    )
    assert s.name == "Test"
    assert s.spotId == "TestID"
    assert isinstance(s.sunriseSunsetTimes, list)
    assert isinstance(s.sunriseSunsetTimes[0], SunriseSunsetTime)
    assert isinstance(s.tideLocation, TideLocation)
    assert isinstance(s.forecasts, list)
    assert isinstance(s.forecasts[0], Forecast)
    assert isinstance(s.tides, list)
    assert isinstance(s.tides[0], Tide)


def test_SpotForecast_get_dataframe():
    s = SpotForecasts(
        "TestID", "Test", FORECASTS, SUNRISESUNSETTIMES, TIDES, TIDELOCATION,
    )
    assert isinstance(s.get_dataframe(), pd.DataFrame)
    assert isinstance(s.get_dataframe("tides"), pd.DataFrame)
    assert isinstance(s.get_dataframe("sunriseSunsetTimes"), pd.DataFrame)


def test_SpotForecast_get_dataframe_unsupported():
    s = SpotForecasts(
        "TestID", "Test", FORECASTS, SUNRISESUNSETTIMES, TIDES, TIDELOCATION,
    )
    with pytest.raises(ValueError):
        s.get_dataframe("unsupported")