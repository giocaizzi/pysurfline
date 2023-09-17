"""api objects models"""
from dataclasses import dataclass
from typing import List
from datetime import datetime as dt
import pandas as pd


@dataclass
class Time:
    timestamp: int

    def __post_init__(self):
        self.timestamp = dt.utcfromtimestamp(self.timestamp)


@dataclass
class Weather:
    temperature: float
    condition: str


@dataclass
class Wind:
    speed: float
    direction: float


@dataclass
class Surf:
    min: float
    max: float


@dataclass
class Swell:
    height: float
    direction: float
    directionMin: float
    period: float


@dataclass
class ForecastLocation:
    name: str
    min: float
    max: float
    lon: float
    lat: float
    mean: float


@dataclass
class Tide:
    timestamp: Time
    type: str
    height: float

    def __post_init__(self):
        self.timestamp = Time(self.timestamp)


@dataclass
class DayLightTimes:
    midnight: Time
    sunrise: Time
    sunset: Time

    def __post_init__(self):
        self.midnight = Time(self.midnight)
        self.sunrise = Time(self.sunrise)
        self.sunset = Time(self.sunset)


@dataclass
class ForecastObject:
    timestamp: int
    weather: Weather
    wind: Wind
    surf: Surf
    swells: List[Swell]

    def __post_init__(self):
        self.timestamp = dt.fromtimestamp(self.timestamp)
        self.weather = Weather(**self.weather)
        self.wind = Wind(**self.wind)
        self.surf = Surf(**self.surf)
        self.swells = [Swell(**item) for item in self.swells]


@dataclass
class SpotForecasts:
    spotId: str
    name: str
    sunriseSunsetTimes: List[DayLightTimes]
    tideLocation: dict
    forecasts: List[ForecastObject]
    tides: List[Tide]

    def __post_init__(self):
        self.sunriseSunsetTimes = [
            DayLightTimes(**item) for item in self.sunriseSunsetTimes
        ]
        self.tideLocation = ForecastLocation(**self.tideLocation)
        self.forecasts = [ForecastObject(**item) for item in self.forecasts]
        self.tides = [Tide(**item) for item in self.tides]

    def get_dataframe(self, attr="forecasts") -> pd.DataFrame:
        """pandas dataframe of selected attribute

        Get the pandas dataframe of the selected attribute. The attribute
        can be:
            - 'forecast'
            - 'tides'
            - 'sunriseSunsetTimes'

        Args:
            attr (str, optional): attribute to get dataframe from.
                Defaults to "forecast".

        Raises:
        """

        if attr == "forecasts":
            data = [item.__dict__ for item in self.forecasts]
        elif attr == "tides":
            data = [item.__dict__ for item in self.tides]
        elif attr == "sunriseSunsetTimes":
            data = [item.__dict__ for item in self.sunriseSunsetTimes]
        else:
            raise ValueError(
                f"Attribute {attr} not supported. Use 'forecast', 'tides'"
                " or 'sunriseSunsetTimes'"
            )
        return pd.DataFrame(data)
