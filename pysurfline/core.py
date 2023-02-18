"""
core classes for basic Surfline API v2 URL requests
"""
import requests
from requests.exceptions import HTTPError
import pandas as pd

from pysurfline.utils import flatten


class SpotForecast:
    """
    Full surfline forecast of given spot.
    Data is stored as class attributes.

    Arguments:
        params (dict): forecast parameters
        verbose (bool): print log

    Attributes:
        api_log (list): api requests log
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

    def __init__(self, params, verbose=False):
        self.params = params
        self.verbose = verbose
        self._get_forecasts()

    def _get_forecasts(self):
        """
        get all types of forecasts setting an attribute for each
        """
        types = ["wave", "wind", "tides", "weather"]
        log = []
        for type in types:
            f = ForecastGetter(type, self.params)
            if f.response.status_code == 200:
                forecast = f.response.json()

                # parse response data
                for key in forecast["data"]:
                    setattr(self, key, forecast["data"][key])

                # parse all associated information
                for key in forecast["associated"]:
                    # units stored with attribute name that refers to
                    # eventually duplicated attr are not overwritten
                    if key in [
                        "units",
                    ] or hasattr(self, key):
                        setattr(self, key + "_" + type, forecast["associated"][key])
                    else:
                        setattr(self, key, forecast["associated"][key])

                # format dates contained ion data
                self._format_attribute(type)
            else:
                print(f"Error : {f.response.status_code}")
                print(f.response.reason)
            if self.verbose:
                print("-----")
                print(f)
            log.append(str(f))
        self.api_log = log

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

    def get_dataframe(self, attr):
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
    WIND_TYPE = "wind"
    WEATHER_TYPE = "weather"
    TIDES_TYPE = "tides"

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
        forecast_type: str = SURF_TYPE,
        days: int = 3,
        interval_hours: int = 3,
    ) -> dict:
        """
        Sends an HTTP request to the Surfline API to retrieve
        the forecast for the specified spot.

        Args:
            forecast_type: The type of forecast requested, can be 'surf',
                'wind', 'weather', or 'tides' (defaults to 'surf').
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
            "type": forecast_type,
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
