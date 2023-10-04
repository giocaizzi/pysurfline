"""api objects: data models"""
from dataclasses import dataclass
from typing import List, Union
from datetime import datetime
import pandas as pd


from .utils import flatten


class Time:
    """time data model

    Attributes:
        timestamp (int): utc timestamp
        dt (datetime): utc naive datetime
    """

    timestamp: int
    dt: datetime = None

    def __init__(self, timestamp: int):
        # utc naive datetime
        self.timestamp = timestamp
        self.dt = datetime.utcfromtimestamp(self.timestamp)

    def __str__(self):
        return f"Time({str(self.dt)})"

    def __repr__(self):
        return str(self)


@dataclass
class Weather:
    """wheter data model"""

    timestamp: Union[int, Time]
    utcOffset: int
    temperature: float
    condition: str
    pressure: int

    def __post_init__(self):
        self.timestamp = Time(self.timestamp)


@dataclass
class Wind:
    """wind data model"""

    timestamp: Union[int, Time]
    utcOffset: int
    speed: float
    direction: float
    directionType: str
    gust: float
    optimalScore: int

    def __post_init__(self):
        self.timestamp = Time(self.timestamp)


@dataclass
class Surf:
    """surf data model"""

    min: float
    max: float
    optimalScore: int
    plus: str
    humanRelation: str
    raw: dict


@dataclass
class Swell:
    """swell data model"""

    height: float
    period: int
    impact: float
    power: float
    direction: float
    directionMin: float
    optimalScore: int


@dataclass
class Wave:
    """wave data model"""

    timestamp: Union[int, Time]
    probability: float
    utcOffset: int
    surf: Union[dict, Surf]
    power: float
    swells: List[Union[dict, Swell]]

    def __post_init__(self):
        self.timestamp = Time(self.timestamp)
        self.surf = Surf(**self.surf)
        self.swells = [Swell(**item) for item in self.swells]


@dataclass
class Tide:
    """tide data model"""

    timestamp: Union[int, Time]
    utcOffset: int
    type: str
    height: float

    def __post_init__(self):
        self.timestamp = Time(self.timestamp)


@dataclass
class SunlightTimes:
    """sunlightTimes data model"""

    midnight: Union[int, Time]
    midnightUTCOffset: int
    dawn: Union[int, Time]
    dawnUTCOffset: int
    sunrise: Union[int, Time]
    sunriseUTCOffset: int
    sunset: Union[int, Time]
    sunsetUTCOffset: int
    dusk: Union[int, Time]
    duskUTCOffset: int

    def __post_init__(self):
        self.midnight = Time(self.midnight)
        self.dawn = Time(self.dawn)
        self.sunrise = Time(self.sunrise)
        self.sunset = Time(self.sunset)
        self.dusk = Time(self.dusk)


# @dataclass
# class SpotForecasts:
#     """spot forecasts data model

#     Composite data model of all the spot forecasts data,
#     - forecasts (surf, weather, wind, swells)
#     - sunrise and sunset times
#     - tides
#     """

#     spotId: str
#     name: str
#     forecasts: List[Forecast]
#     sunriseSunsetTimes: List[SunriseSunsetTime]
#     tides: List[Tide]
#     tideLocation: dict

#     def __post_init__(self):
#         self.sunriseSunsetTimes = [
#             SunriseSunsetTime(**item) for item in self.sunriseSunsetTimes
#         ]
#         self.tideLocation = TideLocation(**self.tideLocation)
#         self.forecasts = [Forecast(**item) for item in self.forecasts]
#         self.tides = [Tide(**item) for item in self.tides]

#     def get_dataframe(self, attr="forecasts") -> pd.DataFrame:
#         """pandas dataframe of selected attribute

#         Get the pandas dataframe of the selected attribute. The attribute
#         can be:
#         - 'forecast'
#         - 'tides'
#         - 'sunriseSunsetTimes'

#         Args:
#             attr (str, optional): attribute to get dataframe from.
#                 Defaults to "forecast".

#         Raises:
#         """

#         if attr == "forecasts":
#             data = [flatten(item.__dict__) for item in self.forecasts]
#         elif attr == "tides":
#             data = [flatten(item.__dict__) for item in self.tides]
#         elif attr == "sunriseSunsetTimes":
#             data = [flatten(item.__dict__) for item in self.sunriseSunsetTimes]
#         else:
#             raise ValueError(
#                 f"Attribute {attr} not supported. Use 'forecast', 'tides'"
#                 " or 'sunriseSunsetTimes'"
#             )
#         return pd.DataFrame(data)
