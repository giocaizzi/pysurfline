"""api functions and classes"""

import requests
import pandas as pd

from .models.spots import Wave, Wind, Weather, SunlightTimes, Tides, Details
from ..utils import flatten


class ApiObject:
    _data: dict = None  # spot/forecasts response
    _associated: dict = None
    _spot: dict = None  # spot/details response
    # permissions : dict = None TODO: add permissions
    _url: str = None
    model_class = None

    def __init__(self, response: requests.Response, model_class=None):
        if "data" in response.json():
            self._data = response.json()["data"]
        if "associated" in response.json():
            self._associated = response.json()["associated"]
        if "spot" in response.json():
            self._spot = response.json()["spot"]
        # urse
        self._url = response.url

        # parse data

        # type(model_class) is Details returns False as it is a class
        # type(model_class) == Details returns True when model_class is an istance
        # of a class
        if model_class is not None:
            self.model_class = model_class
            if self._data is not None:
                self._parse_data(model_class)

    @property
    def data(self):
        return self._data

    @property
    def associated(self):
        return self._associated

    @property
    def spot(self):
        return self._spot

    @property
    def url(self):
        return self._url

    def _parse_data(self, model_class) -> None:
        """parse data into model class"""
        # make keys lowercase
        self._data = {key.lower(): value for key, value in self._data.items()}

        self._data = [
            model_class(**item) for item in self._data[model_class.__name__.lower()]
        ]

    def __str__(self):
        if self.model_class is None:
            return f"ApiObject({self.url})"
        else:
            return f"{self.model_class.__name__}({self.url})"

    def __repr__(self):
        return str(self)


class SpotForecastsWave(ApiObject):
    """spots/forecasts/wave endpoint"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, model_class=Wave)


class SpotForecastsWind(ApiObject):
    """spots/forecasts/wind endpoint"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, model_class=Wind)


class SpotForecastsWeather(ApiObject):
    """spots/forecasts/weather endpoint"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, model_class=Weather)


class SpotForecastsSunlightTimes(ApiObject):
    """spots/forecasts/sunlightTimes endpoint"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, model_class=SunlightTimes)


class SpotForecastsTides(ApiObject):
    """spots/forecasts/tides endpoint"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, model_class=Tides)


class SpotDetails(ApiObject):
    """spots/details endpoint"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, model_class=Details)


class SpotForecasts:
    """spot forecasts data model

    Composite data model of all the spot forecasts data,
    - wave
    - condition (TODO)
    - wind
    - tides
    - weather and sunrise and sunset times

    TODO: add associated data and improve utcOffset
    """

    name: str = None

    def __init__(
        self,
        spotId: str,
        details: SpotDetails,
        waves: SpotForecastsWave,
        winds: SpotForecastsWind,
        tides: SpotForecastsTides,
        sunlightTimes: SpotForecastsSunlightTimes,
        weather: SpotForecastsWeather,
    ):
        self.spotId = spotId
        self.name = details.spot["name"]
        self.waves = waves.data
        self.wind = winds.data
        self.tides = tides.data
        self.weather = weather.data
        self.sunlightTimes = sunlightTimes.data

    def get_dataframe(self, attr="waves") -> pd.DataFrame:
        """pandas dataframe of selected attribute

        Get the pandas dataframe of the selected attribute.

        Args:
            attr (str, optional): attribute to get dataframe from.
                Defaults to "waves".

        Raises:
        """

        if attr == "all":
            raise NotImplementedError("all not implemented yet")
        elif attr in ["waves", "wind", "tides", "weather", "sunlightTimes"]:
            data = [flatten(item.__dict__) for item in getattr(self, attr)]
        else:
            raise ValueError(f"Attribute {attr} not supported. Use a valid attribute.")
        return pd.DataFrame(data)
