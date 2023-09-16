"""
core classes for basic Surfline API v2 URL requests
"""
import requests

from .models import SpotForecast


def get_spot_forecast(spotId: str) -> SpotForecast:
    """get spot forecast

    Get forecast for given spot by passing the spotId
    argument.

    Arguments:
        spotId (str): spot id

    Returns:
        forecast (:obj:`SpotForecast`)
    """
    return SurflineClient()._get_spot_forecast(spotId)


class SurflineClient:
    _baseurl: str = "https://services.surfline.com/kbyg/"

    def __init__(self):
        pass

    def _get_spot_forecast(self, spotId: str):
        return SpotForecast(
            spotId,
            **APIGetter(self, "spots/forecasts").get(params={"spotId": spotId}).data,
        )


class APIGetter:
    """
    Class for Surfline V2 REST API GET requests.

    Arguments:
        client (SurflineAPIClient): Surfline API client
        endpoint (str): API endpoint

    Attributes:
        client (SurflineAPIClient): Surfline API client
        endpoint (str): API endpoint
        response (requests.Response): response object
        url (str): response url
        data (dict): response data
        status_code (int): response status code
    """

    response: requests.Response = None

    def __init__(self, client: SurflineClient, endpoint: str):
        self._client = client
        self._endpoint = endpoint

    def get(self, params=None, headers=None):
        """
        get response from request.
        Handles HTTP errors and connection errors.
        """
        try:
            self.response = requests.get(
                self._client._baseurl + self._endpoint, params=params, headers=headers
            )
            self.response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error occurred: {e}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
        return self

    @property
    def url(self):
        return self.response.url

    @property
    def data(self):
        return self.response.json()["data"]

    @property
    def status_code(self):
        return self.response.status_code

    def __str__(self):
        return f"APIGetter(endpoint:{self._endpoint},status:{self.status_code})"

    def __repr__(self):
        return str(self)
