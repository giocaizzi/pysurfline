"""
core classes for basic Surfline API v2 URL requests
"""
import requests
from requests.exceptions import HTTPError
import pandas as pd


class SpotForecast:
    """
    Custom object representing the forecast of a single spot.
    Data is stored as class attributes.

    Attributes:
        spot_id (str): surfline spot id
        json (:obj:`pysurfline.core.SurflineAPI`): original API response
        sunriseSunsetTimes (:obj:`pd.DataFrame`): sunlight times
        forecast (:obj:`pd.DataFrame`): surf forecast
        tideLocation (:obj:`pd.DataFrame`) : location where tide is computed
        tides (:obj:`pd.DataFrame`): tides forecast
    """

    def __init__(self, spot_id: str):
        """
        Initialize the SpotForecast object with a `spot_id` argument.

        Args:
            spot_id (str): surfline spot id
        """
        self.spot_id = spot_id

    def load_forecast(self, **kwargs):
        """
        loads spot forecast, setting an attribute for each.

        Args:
            \\**kwargs: keyword arguments passed to 'SurflineAPI.get_forecast' method.
        """
        self.json = SurflineAPI(self.spot_id).get_forecast(**kwargs)
        for key in self.json["data"]:
            setattr(self, key, pd.json_normalize(self.json["data"][key]))


class SurflineAPI:
    """Wrapper for the Surfline API.

    Attributes:
        spot_id (str): surfline spotid code
        endpoint (str): endpoint url
    """

    def __init__(self, spot_id: str):
        """
        Initializes the API object with the spot ID code.

        Args:
            spot_id: The ID of the spot.
        """
        self.spot_id = spot_id
        self.endpoint = "https://services.surfline.com/kbyg/spots/forecasts?"

    # might be that api has been changed and the parameters disabled
    # response seems to be the same
    def get_forecast(
        self,
        days: int = 3,
        interval_hours: int = 3,
    ) -> dict:
        """
        Sends an HTTP request to the Surfline API to retrieve
        the forecast for the specified spot.

        Args:
            interval_hours (int): The number of hours between each
                forecast data point. Defaults to 3.
            days: The number of forecast days requested (defaults to 3).

        Returns:
            A dictionary containing the forecast data.

        Raises:
            HTTPError: If the HTTP request returns an error status code.
            ValueError: If an error occurs while processing
                the response data.
        """
        params = {
            "spotId": self.spot_id,
            "type": "surf",
            "days": days,
            "interval_hours": interval_hours,
        }
        response = requests.get(self.endpoint, params=params)

        try:
            response.raise_for_status()
            return response.json()
        except HTTPError as http_err:
            raise HTTPError(f"HTTP error occurred: {http_err}")
        except Exception as err:
            raise ValueError(f"Error occurred: {err}")
