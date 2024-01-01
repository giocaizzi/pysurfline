"""api functions and classes"""

import requests

from .models.spots import Wave, Wind, Weather, SunlightTimes, Tides, Details


class ApiResponseObject:
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


class SpotForecastsWave(ApiResponseObject):
    """spots/forecasts/wave endpoint"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, model_class=Wave)


class SpotForecastsWind(ApiResponseObject):
    """spots/forecasts/wind endpoint"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, model_class=Wind)


class SpotForecastsWeather(ApiResponseObject):
    """spots/forecasts/weather endpoint"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, model_class=Weather)


class SpotForecastsSunlightTimes(ApiResponseObject):
    """spots/forecasts/sunlightTimes endpoint"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, model_class=SunlightTimes)


class SpotForecastsTides(ApiResponseObject):
    """spots/forecasts/tides endpoint"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, model_class=Tides)


class SpotDetails(ApiResponseObject):
    """spots/details endpoint"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, model_class=Details)
