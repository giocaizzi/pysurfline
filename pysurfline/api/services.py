from pysurfline.api.objects import (
    ApiResponseObject,
    SpotForecastsSunlightTimes,
    SpotForecastsTides,
    SpotForecastsWave,
    SpotForecastsWeather,
    SpotForecastsWind,
    SpotDetails,
)


import requests
from typing import Tuple, Union


class ApiService:
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

    _client = None
    _endpoint: str = None
    response: requests.Response = None

    def __init__(self, client, endpoint: str):
        self._client = client
        self._endpoint = endpoint

    def get(self, params=None) -> ApiResponseObject:
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
    ) -> Union[ApiResponseObject, Tuple[ApiResponseObject, ApiResponseObject]]:
        if self._endpoint == "spots/forecasts/wave":
            return SpotForecastsWave(self.response)
        elif self._endpoint == "spots/forecasts/wind":
            return SpotForecastsWind(self.response)
        elif self._endpoint == "spots/forecasts/weather":
            return SpotForecastsWeather(self.response), SpotForecastsSunlightTimes(
                self.response
            )
        elif self._endpoint == "spots/forecasts/tides":
            return SpotForecastsTides(self.response)
        elif self._endpoint == "spots/details":
            return SpotDetails(self.response)
        else:
            raise NotImplementedError(
                "A child APIObject class is not implemented for this endpoint."
            )

    def __str__(self):
        return f"ApiService(endpoint:{self._endpoint},response:{str(self.response)})"

    def __repr__(self):
        return str(self)
