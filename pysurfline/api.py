"""
api functional objects and methods
"""
import requests

from .models import SpotForecasts


def get_spot_forecasts(spotId: str) -> SpotForecasts:
    """get spot forecast

    Get forecast for given spot by passing the spotId
    argument.

    Arguments:
        spotId (str): spot id

    Returns:
        forecast (:obj:`SpotForecast`)
    """
    return SurflineClient()._get_spot_forecasts(spotId)


class SurflineClient:
    _baseurl: str = "https://services.surfline.com/kbyg/"

    def __init__(self):
        pass

    def _get_spot_forecasts(self, spotId: str) -> SpotForecasts:
        """create a SpotForecast object from API responses"""
        return SpotForecasts(
            spotId,
            **APIResource(self, "spots/details")
            .get(params={"spotId": spotId})
            .json["spot"],
            **APIResource(self, "spots/forecasts")
            .get(params={"spotId": spotId})
            .json["data"],
        )


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
        url (str): response url
        data (dict): response data
        status_code (int): response status code
    """
    _client: SurflineClient = None
    _endpoint: str = None
    response: requests.Response = None

    def __init__(self, client: SurflineClient, endpoint: str):
        self._client = client
        self._endpoint = endpoint

    def get(self, params=None, headers=None):
        """
        get response from request.
        Handles HTTP errors and connection errors.

        Arguments:
            params (dict): request parameters
            headers (dict): request headers

        Returns:
            self (:obj:`APIGetter`)

        Raises:
            requests.exceptions.HTTPError: if HTTP error occurs
            requests.exceptions.ConnectionError: if connection error occurs
            requests.exceptions.RequestException: if other error occurs
        """
        try:
            self.response = requests.get(
                self._client._baseurl + self._endpoint, params=params, headers=headers
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
        return self


    @property
    def url(self):
        return self.response.url

    @property
    def json(self):
        return self.response.json()

    @property
    def status_code(self):
        return self.response.status_code

    def __str__(self):
        return f"APIResource(endpoint:{self._endpoint},status:{self.status_code})"

    def __repr__(self):
        return str(self)
