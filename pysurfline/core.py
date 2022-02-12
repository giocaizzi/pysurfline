"""
core classes for basic Surfline API v2 URL requests
"""


class SpotForecast:
    def __init__(self, forecast):
        """
        custom response object of Surfline API forecast for specific spot

        Arguments:
            forecast (dict): dict from Surfline API `requests` response object

        Attributes:
            wave (list): list of wave forecast
            units (dict) :
            utcOffset (int) :
            location (dict) :
            forecastLocation (dict) :
            offshoreLocation (dict) :

        """
        self._forecast = forecast

        # parse response data
        for key in self._forecast["data"]:
            setattr(self, key, self._forecast["data"][key])
        # parse all associated information
        for key in self._forecast["associated"]:
            setattr(self, key, self._forecast["associated"][key])
