"""
core classes for basic Surfline API v2 URL requests
"""
import requests
from requests.exceptions import HTTPError
import pandas as pd

from pysurfline.utils import flatten


class SpotForecast:
    """
    Custom object representing the forecast of a single spot.
    Data is stored as class attributes.

    Attributes:
        api (:obj:`pysurfline.core.SurflineAPI`): original API object
        forecastLocation (dict) : forecast location
        location (dict) : spot location
        offshoreLocation (dict) : location where wave are forecasted
        params (dict) : forecast parameters
        sunlightTimes (list): sunlight times (sunrise,sunset)
        tideLocation (dict) : location where tide is computed
        tides (list): list of tides forecast
        units_tides (dict) : tides units
        units_wave (dict) : wave units
        units_weather (dict) : weather units
        units_wind (dict) : wind units
        utcOffset (int) : utc offset
        verbose (bool) : print log
        wave (list): list of wave forecast
        weather (list): list of weather forecast
        weatherIconPath :
        wind (list): list of wind forecast
    """

    def __init__(self, spot_id: str):
        """
        Initialize the SpotForecast object with a `spot_id` argument.

        Args:
            spot_id (str): _description_
        """
        self.spot_id = spot_id

    def load_forecast(self, **kwargs):
        """
        loads spot forecast, setting an attribute for each

        Args:
            **kwargs: keyword arguments passed to 'SurflineAPI.get_forecast' method.
        """
        self.api = SurflineAPI(self.spot_id).get_forecast(**kwargs)
        for key in self.api["data"]:
            setattr(self, key, self.api["data"][key])
        # format dates contained ion data
        # self._format_attribute(type)

    def _format_attribute(self, type):
        """
        format attribute to more readable format.

        - flattens nested dictionaries, preserving lists

        Arguments:
            type (str): string name of attribute to format eg. wave, tides
        """
        for i in range(len(getattr(self, type))):
            if type == "wave":
                getattr(self, type)[i] = flatten(getattr(self, type)[i])

    def get_dataframe(self, attr: str):
        """
        returns requested attribute as pandas dataframe

        Arguments:
            attr (str): attribute to get eg. wave, tide

        Returns:
            df (:obj:`pandas.DataFrame`)
        """
        if isinstance(getattr(self, attr), list):
            df = pd.DataFrame(getattr(self, attr))
            if "midnight" in df.columns.tolist():
                for t in ["midnight", "dawn", "sunrise", "sunset", "dusk"]:
                    df[t] = pd.to_datetime(df[t], unit="s")
                # df.set_index("midnight",inplace=True)
            else:
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
                df.set_index("timestamp", inplace=True)
            return df
        else:
            raise TypeError("Must be a list.")


class SurflineAPI:
    """Wrapper for the Surfline API."""

    BASE_URL = "https://services.surfline.com/kbyg/spots/forecasts"
    SURF_TYPE = "surf"

    def __init__(self, spot_id: str):
        """
        Initializes the API object with the spot ID code.

        Args:
            spot_id: The ID of the spot.
        """
        self.spot_id = spot_id
        self.endpoint = f"{self.BASE_URL}?"

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
