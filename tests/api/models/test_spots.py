"""Unit tests for models.py"""

from datetime import datetime
import pytz
from pysurfline.api.models.spots import (
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

TEST_TIME = datetime(2021, 8, 24, 16, 20, tzinfo=pytz.utc)

TIMESTAMP = TEST_TIME.timestamp()
EXPECTED_TIME = datetime(2021, 8, 24, 16, 20)

UTC_OFFSET = -25200


def test_time():
    time = Time(TIMESTAMP)
    assert time.timestamp == TIMESTAMP
    assert time.dt == EXPECTED_TIME


def test_weather():
    weather = Weather(TIMESTAMP, UTC_OFFSET, 20.0, "Sunny", 1013)
    assert weather.timestamp.dt == EXPECTED_TIME
    assert weather.utcOffset == UTC_OFFSET
    assert weather.temperature == 20.0
    assert weather.condition == "Sunny"
    assert weather.pressure == 1013


def test_wind():
    wind = Wind(TIMESTAMP, UTC_OFFSET, 10.0, 180.0, "N", 15.0, 5)
    assert wind.timestamp.dt == EXPECTED_TIME
    assert wind.utcOffset == UTC_OFFSET
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
        TIMESTAMP,
        0.8,
        UTC_OFFSET,
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
    assert wave.timestamp.dt == EXPECTED_TIME
    assert wave.probability == 0.8
    assert wave.utcOffset == UTC_OFFSET
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
    tides = Tides(TIMESTAMP, UTC_OFFSET, "high", 1.5)
    assert tides.timestamp.dt == EXPECTED_TIME
    assert tides.utcOffset == UTC_OFFSET
    assert tides.type == "high"
    assert tides.height == 1.5


def test_sunlight_times():
    sunlight_times = SunlightTimes(
        TIMESTAMP,
        UTC_OFFSET,
        TIMESTAMP,
        UTC_OFFSET,
        TIMESTAMP,
        UTC_OFFSET,
        TIMESTAMP,
        UTC_OFFSET,
        TIMESTAMP,
        UTC_OFFSET,
    )
    assert sunlight_times.midnight.dt == EXPECTED_TIME
    assert sunlight_times.midnightUTCOffset == UTC_OFFSET
    assert sunlight_times.dawn.dt == EXPECTED_TIME
    assert sunlight_times.dawnUTCOffset == UTC_OFFSET
    assert sunlight_times.sunrise.dt == EXPECTED_TIME
    assert sunlight_times.sunriseUTCOffset == UTC_OFFSET
    assert sunlight_times.sunset.dt == EXPECTED_TIME
    assert sunlight_times.sunsetUTCOffset == UTC_OFFSET
    assert sunlight_times.dusk.dt == EXPECTED_TIME
    assert sunlight_times.duskUTCOffset == UTC_OFFSET


def test_details():
    details = Details("Test Spot")
    assert details.name == "Test Spot"
