"""
core classes for basic Surfline API v2 URL requests
"""
import datetime
import pandas as pd
from pysurfline.utils import flatten

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

        #format dates contained ion data 
        self._format_attribute("wave")


    def _format_attribute(self,attr):
        """
        format attribute to more readable format.

        - dates from integer timestamp to datetime
        - flattened dictionary, preserving lists

        Arguments:
            attr (str): attribute to format eg. wave, tide
        """
        for i in range(len(getattr(self,attr))):
            getattr(self,attr)[i]=flatten(getattr(self,attr)[i])
            getattr(self,attr)[i]["timestamp"]= datetime.datetime.fromtimestamp(self.wave[i]["timestamp"])

    def get_dataframe(self,attr):
        """
        returns requested attribute as pandas dataframe

        Arguments:
            attr (str): attribute to get eg. wave, tide

        Returns:
            df (:obj:`pandas.DataFrame`)
        """
        if isinstance(getattr(self,attr),list):
            return pd.DataFrame(getattr(self,attr))
        else:
            raise TypeError("Must be a dictionary")

class URLBuilder:
    def __init__(self,type,params):
        self.type=type
        self.params=params
        self._build()
        
    
    def _build(self):
        stringparams=""
        for k,v in self.params.items():
            if stringparams:
                stringparams=stringparams+"&"+k+"="+v
            else:
                stringparams=k+"="+v
        self.url=f"https://services.surfline.com/kbyg/spots/forecasts/{self.type}?{stringparams}"