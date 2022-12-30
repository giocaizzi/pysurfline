"""
core classes for basic Surfline API v2 URL requests
"""
import requests
import pandas as pd

from pysurfline.utils import flatten


class SpotForecast:
    """
    Surfline forecast of given spot.

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


class ForecastGetter:
    """
    Getter of specific forecast type (:obj:`wave`,
    :obj:`wind`, :obj:`tides`, :obj:`weather`).

    Arguments:
        type (str): type of forecast to get :obj:`wave`,
            :obj:`wind`, :obj:`tides`, :obj:`weather`
        params (dict): dictonary of forecast parameters

    Attributes:
        baseurl (str) : URL built by :obj:`pysurfline.URLBuilder` object.
        response (:obj:`requests.response`): A :obj:`request.response` object.
        type (str): type of forecast to get ( :obj:`wave`, :obj:`wind`,
            :obj:`tides`, :obj:`weather`)
        params (dict): dictonary for request of forecast parameters
    """

    def __init__(self, type: str, params: dict):
        self.type = type
        self.params = params
        self.baseurl = "https://services.surfline.com/kbyg/spots/forecasts/"
        self.response = requests.get(self.baseurl + self.type, params=params)
        self.url = self.response.url

    def __repr__(self):
        return f"ForecastGetter(Type:{self.type}, Status:{self.response.status_code})"

    def __str__(self):
        return f"ForecastGetter(Type:{self.type}, Status:{self.response.status_code})"
