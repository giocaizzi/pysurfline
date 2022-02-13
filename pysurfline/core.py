"""
core classes for basic Surfline API v2 URL requests
"""
import requests
import datetime
import pandas as pd
from pysurfline.utils import flatten

class SpotForecast:
    def __init__(self,type,params):
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
        self.type=type
        self.params = params
        self.get_forecast()

    def __str__(self):
        return f"SpotForecast(Type:{self.type}, Status:{self.status_code})"

    def get_forecast(self):
        u=URLBuilder(self.type,self.params)
        self.url=u.url
        r = requests.get(self.url)
        self.status_code=r.status_code
        if self.status_code==200: 
            self._forecast=r.json()

            # parse response data
            for key in self._forecast["data"]:
                setattr(self, key, self._forecast["data"][key])

            # parse all associated information
            for key in self._forecast["associated"]:
                setattr(self, key, self._forecast["associated"][key])

            #format dates contained ion data 
            self._format_attribute()
        else:
            print(f"Error : {self.status_code}")
            print(r.reason)


    def _format_attribute(self):
        """
        format attribute to more readable format.

        - flattened dictionary, preserving lists

        Arguments:
            attr (str): attribute to format eg. wave, tide
        """
        for i in range(len(getattr(self,self.type))):
            if self.type=="wave":
                getattr(self,self.type)[i]=flatten(getattr(self,self.type)[i])

    def get_dataframe(self,attr):
        """
        returns requested attribute as pandas dataframe

        Arguments:
            attr (str): attribute to get eg. wave, tide

        Returns:
            df (:obj:`pandas.DataFrame`)
        """
        if isinstance(getattr(self,attr),list):
            df=pd.DataFrame(getattr(self,attr))
            df['timestamp'] = pd.to_datetime(df['timestamp'],unit='s')
            return df
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