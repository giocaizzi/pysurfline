"""Unit tests for models.py"""
from datetime import datetime
from pysurfline.api.spots.models import (
    Time,
    Weather,
    Wind,
    Surf,
    Swell,
    Wave,
    Tides,
    SunlightTimes,
    Details,
)


def test_time():
    timestamp = 1629822000
    time = Time(timestamp)
    assert time.timestamp == timestamp
    assert time.dt == datetime(2021, 8, 24, 14, 33, 20)


def test_weather():
    weather = Weather(1629822000, -25200, 20.0, "Sunny", 1013)
    assert weather.timestamp.dt == datetime(2021, 8, 24, 14, 33, 20)
    assert weather.utcOffset == -25200
    assert weather.temperature == 20.0
    assert weather.condition == "Sunny"
    assert weather.pressure == 1013


def test_wind():
    wind = Wind(1629822000, -25200, 10.0, 180.0, "N", 15.0, 5)
    assert wind.timestamp.dt == datetime(2021, 8, 24, 14, 33, 20)
    assert wind.utcOffset == -25200
    assert wind.speed == 10.0
    assert wind.direction == 180.0
    assert wind.directionType == "N"
    assert wind.gust == 15.0
    assert wind.optimalScore == 5


def test_surf():
    surf = Surf(1.0, 2.0, 5, "3ft+", "Fun", {})
    assert surf.min == 1.0
    assert surf.max == 2.0
    assert surf.optimalScore == 5
    assert surf.plus == "3ft+"
    assert surf.humanRelation == "Fun"
    assert surf.raw == {}


def test_swell():
    swell = Swell(2.0, 10, 3.0, 4.0, 180.0, 170.0, 5)
    assert swell.height == 2.0
    assert swell.period == 10
    assert swell.impact == 3.0
    assert swell.power == 4.0
    assert swell.direction == 180.0
    assert swell.directionMin == 170.0
    assert swell.optimalScore == 5


def test_wave():
    wave = Wave(
        1629822000,
        0.8,
        -25200,
        {
            "min": 1.0,
            "max": 2.0,
            "optimalScore": 5,
            "plus": "3ft+",
            "humanRelation": "Fun",
            "raw": {},
        },
        4.0,
        [
            {
                "height": 2.0,
                "period": 10,
                "impact": 3.0,
                "power": 4.0,
                "direction": 180.0,
                "directionMin": 170.0,
                "optimalScore": 5,
            }
        ],
    )
    assert wave.timestamp.dt == datetime(2021, 8, 24, 14, 33, 20)
    assert wave.probability == 0.8
    assert wave.utcOffset == -25200
    assert wave.surf.min == 1.0
    assert wave.surf.max == 2.0
    assert wave.surf.optimalScore == 5
    assert wave.surf.plus == "3ft+"
    assert wave.surf.humanRelation == "Fun"
    assert wave.surf.raw == {}
    assert wave.power == 4.0
    assert wave.swells[0].height == 2.0
    assert wave.swells[0].period == 10
    assert wave.swells[0].impact == 3.0
    assert wave.swells[0].power == 4.0
    assert wave.swells[0].direction == 180.0
    assert wave.swells[0].directionMin == 170.0
    assert wave.swells[0].optimalScore == 5


def test_tides():
    tides = Tides(1629822000, -25200, "high", 1.5)
    assert tides.timestamp.dt == datetime(2021, 8, 24, 14, 33, 20)
    assert tides.utcOffset == -25200
    assert tides.type == "high"
    assert tides.height == 1.5


def test_sunlight_times():
    sunlight_times = SunlightTimes(
        1629822000,
        -25200,
        1629800000,
        -25200,
        1629800000,
        -25200,
        1629860000,
        -25200,
        1629860000,
        -25200,
    )
    assert sunlight_times.midnight.dt == datetime(2021, 8, 24, 0, 0)
    assert sunlight_times.midnightUTCOffset == -25200
    assert sunlight_times.dawn.dt == datetime(2021, 8, 24, 6, 0)
    assert sunlight_times.dawnUTCOffset == -25200
    assert sunlight_times.sunrise.dt == datetime(2021, 8, 24, 6, 0)
    assert sunlight_times.sunriseUTCOffset == -25200
    assert sunlight_times.sunset.dt == datetime(2021, 8, 24, 18, 0)
    assert sunlight_times.sunsetUTCOffset == -25200
    assert sunlight_times.dusk.dt == datetime(2021, 8, 24, 18, 0)
    assert sunlight_times.duskUTCOffset == -25200


def test_details():
    details = Details("Test Spot")
    assert details.name == "Test Spot"
