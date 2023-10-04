"""api functions and classes"""

import requests

from .client import SurflineClient
from .models import Wave, Wind, Weather, SunlightTimes, Tide


class GenericResponse:
    _data: dict = None
    _associated: dict = None
    # permissions : dict = None TODO: add permissions
    _url: str = None
    model_class = None

    def __init__(self, response: requests.Response, model_class=None):
        self._data = response.json()["data"]
        self._associated = response.json()["associated"]
        self._url = response.url
        # parse data
        if model_class is not None:
            self.model_class = model_class
            self.parse_data(model_class)

    @property
    def data(self):
        return self._data

    def parse_data(self, model_class) -> None:
        self._data = [
            model_class(**item) for item in self._data[model_class.__name__.lower()]
        ]

    @property
    def associated(self):
        return self._associated

    @property
    def url(self):
        return self._url

    def __str__(self):
        if self.model_class is None:
            return f"GenericResponse({self.url})"
        else:
            return f"{self.model_class.__name__}({self.url})"

    def __repr__(self):
        return str(self)


class WaveResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, model_class=Wave)


class WindResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, model_class=Wind)


class WeatherResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, model_class=Weather)


class SunlightTimesResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, model_class=SunlightTimes)


class TidesResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, model_class=Tide)


class APIResource:
    """
    Class for Surfline V2 REST API resources.

    Arguments:
        client (SurflineAPIClient): Surfline API client
        endpoint (str): API endpoint of service

    Attributes:
        client (SurflineAPIClient): Surfline API client
        endpoint (str): API endpoint
        response (requests.Response): response object
    """

    _client: SurflineClient = None
    _endpoint: str = None
    response: requests.Response = None

    def __init__(self, client: SurflineClient, endpoint: str):
        self._client = client
        self._endpoint = endpoint

    def get(self, params=None) -> GenericResponse:
        """
        get response from request.
        Handles HTTP errors and connection errors.

        Arguments:
            params (dict): request parameters

        Returns:
            APIResponse: response object

        Raises:
            requests.exceptions.HTTPError: if HTTP error occurs
            requests.exceptions.ConnectionError: if connection error occurs
            requests.exceptions.RequestException: if other error occurs
        """
        try:
            self.response = requests.get(
                self._client._baseurl + self._endpoint,
                params=params,
            )
            self.response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("HTTP error occurred!")
            raise e
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred!")
            raise e
        except requests.exceptions.RequestException as e:
            print("An request error occurred!")
            return e
        except Exception as e:
            print("An error occurred!")
            raise e
        return self._return_modelled_response()

    def _return_modelled_response(
        self,
    ) -> GenericResponse:
        if self._endpoint == "spots/forecasts/wave":
            return WaveResponse(self.response)
        elif self._endpoint == "spots/forecasts/wind":
            return WindResponse(self.response)
        elif self._endpoint == "spots/forecasts/weather":
            return WeatherResponse(self.response)
        elif self._endpoint == "spots/forecasts/tides":
            return TidesResponse(self.response)
        else:
            raise NotImplementedError(
                "A child BaseResponse class is not implemented for this endpoint."
            )

    def __str__(self):
        return f"APIResource(endpoint:{self._endpoint},response:{str(self.response)})"

    def __repr__(self):
        return str(self)
