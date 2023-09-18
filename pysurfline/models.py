"""api objects: data models"""
from dataclasses import dataclass
from typing import List
from datetime import datetime
import pandas as pd

from .utils import flatten


@dataclass
class Time:
    """time data model

    Attributes:
        timestamp (int): utc timestamp
        dt (datetime): utc naive datetime
    """

    timestamp: int
    dt: datetime = None

    def __post_init__(self):
        # utc naive datetime
        self.dt = datetime.utcfromtimestamp(self.timestamp)


@dataclass
class Weather:
    """wheter data model"""

    temperature: float
    condition: str


@dataclass
class Wind:
    """wind data model"""

    speed: float
    direction: float


@dataclass
class Surf:
    """surf data model"""

    min: float
    max: float


@dataclass
class Swell:
    """swell data model"""

    height: float
    direction: float
    directionMin: float
    period: float


@dataclass
class TideLocation:
    """tide location data model"""

    name: str
    min: float
    max: float
    lon: float
    lat: float
    mean: float


@dataclass
class Tide:
    """tide data model"""

    timestamp: Time
    type: str
    height: float

    def __post_init__(self):
        self.timestamp = Time(self.timestamp)


@dataclass
class SunriseSunsetTime:
    """daylight data model"""

    midnight: Time
    sunrise: Time
    sunset: Time

    def __post_init__(self):
        self.midnight = Time(self.midnight)
        self.sunrise = Time(self.sunrise)
        self.sunset = Time(self.sunset)


@dataclass
class Forecast:
    """forecast data model

    Composite data model of all the forecast data.
    Associated to a specific timestamp of type `Time`.
    """

    timestamp: Time
    weather: Weather
    wind: Wind
    surf: Surf
    swells: List[Swell]

    def __post_init__(self):
        self.timestamp = Time(self.timestamp)
        self.weather = Weather(**self.weather)
        self.wind = Wind(**self.wind)
        self.surf = Surf(**self.surf)
        self.swells = [Swell(**item) for item in self.swells]


@dataclass
class SpotForecasts:
    """spot forecasts data model

    Composite data model of all the spot forecasts data,
    - forecasts (surf, weather, wind, swells)
    - sunrise and sunset times
    - tides
    """

    spotId: str
    name: str
    forecasts: List[Forecast]
    sunriseSunsetTimes: List[SunriseSunsetTime]
    tides: List[Tide]
    tideLocation: dict

    def __post_init__(self):
        self.sunriseSunsetTimes = [
            SunriseSunsetTime(**item) for item in self.sunriseSunsetTimes
        ]
        self.tideLocation = TideLocation(**self.tideLocation)
        self.forecasts = [Forecast(**item) for item in self.forecasts]
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
            data = [flatten(item.__dict__) for item in self.forecasts]
        elif attr == "tides":
            data = [flatten(item.__dict__) for item in self.tides]
        elif attr == "sunriseSunsetTimes":
            data = [flatten(item.__dict__) for item in self.sunriseSunsetTimes]
        else:
            raise ValueError(
                f"Attribute {attr} not supported. Use 'forecast', 'tides'"
                " or 'sunriseSunsetTimes'"
            )
        return pd.DataFrame(data)
