"""spot forecast class"""
from dataclasses import dataclass
from typing import List
from datetime import datetime as dt


@dataclass
class DayLightTimes:
    midnight: int
    sunrise: int
    sunset: int

    def __post_init__(self):
        self.midnight = dt.fromtimestamp(self.midnight)
        self.sunrise = dt.fromtimestamp(self.sunrise)
        self.sunset = dt.fromtimestamp(self.sunset)

@dataclass
class ForecastLocation:
    name: str
    min: float
    max: float
    lon: float
    lat: float
    mean: float


@dataclass
class SpotForecast:
    spotId: str
    sunriseSunsetTimes: List[DayLightTimes]
    tideLocation: dict
    forecasts: list
    tides: list

    def __post_init__(self):
        self.sunriseSunsetTimes = [
            DayLightTimes(**item) for item in self.sunriseSunsetTimes
        ]
        self.tideLocation = ForecastLocation(**self.tideLocation)
