"""
core classes for basic Surfline API v2 URL requests
"""
from tabnanny import verbose
import requests
import pandas as pd
from pysurfline.utils import flatten,degToCompass
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates
import datetime
import pandas as pd
import numpy as np
import matplotlib.patheffects as pe

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

    def __init__(self,params,verbose=False):
        self.params = params
        self.verbose=verbose
        self._get_forecasts()

    def _get_forecasts(self):
        """
        get all types of forecasts setting an attribute for each
        """
        types=["wave","wind","tides","weather"]
        log=[]
        for type in types:
            f=ForecastGetter(type,self.params)
            if f.response.status_code==200: 
                forecast=f.response.json()

                # parse response data
                for key in forecast["data"]:
                    setattr(self, key, forecast["data"][key])

                # parse all associated information
                for key in forecast["associated"]:
                    #units stored with attribute name that refers to
                    #eventually duplicated attr are not overwritten
                    if key in ["units",] or hasattr(self,key):
                        setattr(self, key+"_"+type, forecast["associated"][key])
                    else:
                        setattr(self, key, forecast["associated"][key])

                #format dates contained ion data 
                self._format_attribute(type)
            else:
                print(f"Error : {f.response.status_code}")
                print(f.response.reason)
            if self.verbose:
                print("-----")
                print(f)
            log.append(str(f))
        self.api_log=log

    def _format_attribute(self,type):
        """
        format attribute to more readable format.

        - flattens nested dictionaries, preserving lists

        Arguments:
            type (str): string name of attribute to format eg. wave, tides
        """
        for i in range(len(getattr(self,type))):
            if type=="wave":
                getattr(self,type)[i]=flatten(getattr(self,type)[i])

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
            if "midnight" in df.columns.tolist():
                for t in ["midnight","dawn","sunrise","sunset","dusk"]:
                    df[t] = pd.to_datetime(df[t],unit='s')
                # df.set_index("midnight",inplace=True)
            else:
                df['timestamp'] = pd.to_datetime(df['timestamp'],unit='s')
                df.set_index("timestamp",inplace=True)
            return df
        else:
            raise TypeError("Must be a list.")

class ForecastGetter:
    """
    Getter of specific forecast type (:obj:`wave`, :obj:`wind`, :obj:`tides`, :obj:`weather`).

    Arguments:
        type (str): type of forecast to get :obj:`wave`, :obj:`wind`, :obj:`tides`, :obj:`weather`
        params (dict): dictonary of forecast parameters   
    
    Attributes:
        url (str) : URL built by :obj:`pysurfline.URLBuilder` object.
        response (:obj:`requests.response`): A :obj:`request.response` object.
        type (str): type of forecast to get ( :obj:`wave`, :obj:`wind`, :obj:`tides`, :obj:`weather`)
        params (dict): dictonary of forecast parameters     
    """
    def __init__(self,type,params):
        self.type=type
        self.params=params
        u=URLBuilder(self.type,self.params)
        self.url=u.url
        self.response = requests.get(self.url)

    def __repr__(self):
        return f"ForecastGetter(Type:{self.type}, Status:{self.response.status_code})"

    def __str__(self):
        return f"ForecastGetter(Type:{self.type}, Status:{self.response.status_code})"

class URLBuilder:
    """
    Build URL for Surfline v2 API

    Arguments:
        type (str): type of forecast to get `wave`,`wind`,`tides`,`weather`
        params (dict): dictonary of forecast parameters

    Attributes:
        url(str): URL of desired forecast
        type (str): type of forecast URL to get ( :obj:`wave`, :obj:`wind`, :obj:`tides`, :obj:`weather` )
        params (dict): dictonary of forecast URL parameters  
    """
    def __init__(self,type,params):
        self.type=type
        self.params=params
        self._build()
        
    def _build(self):
        """
        build URL
        """
        stringparams=""
        for k,v in self.params.items():
            if stringparams:
                stringparams=stringparams+"&"+k+"="+str(v)
            else:
                stringparams=k+"="+str(v)
        self.url=f"https://services.surfline.com/kbyg/spots/forecasts/{self.type}?{stringparams}"


class SurfReport(SpotForecast):
    """
    Structured spot surf-report object.
    """
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self._set_df()
        self._get_simple_surf_report()

    def _set_df(self):
        df = []
        for attr in ["wave", "wind","weather",]:  # exclude "tides" because of HIGH LOW exact times
            df.append(self.get_dataframe(attr))
        df = pd.concat(df, axis=1)
        self.df = df

    def _get_simple_surf_report(self):
        self.surf = self.df.copy()[["surf_min", "surf_max", "speed", "directionType","direction"]]
        #set Hmin <0.2m to nan for plotting reasons
        self.surf.loc[(self.df["surf_min"]<0.2),"surf_min"]=np.nan

    def plot(self):
        f, ax = plt.subplots(dpi=300)
        surf_colors = {"Hmax": "dodgerblue", "Hmin": "lightblue"}
        wind_colors = {"Cross-shore": "coral", "Offshore": "green", "Onshore": "darkred"}
        daylight = self.get_dataframe("sunlightTimes")

        #scale parameter
        hmax=self.surf["surf_max"].max()
        hmax=hmax*1.2
        if hmax<2:
            hmax=2

        # zorder 0
        # night and day
        for i, x in daylight.iterrows():
            ax.axvspan(x["midnight"], x["dawn"], color="darkgrey", zorder=0)
            ax.axvspan(x["dawn"], x["sunrise"], color="lightgrey", zorder=0)
            ax.axvspan(x["sunset"], x["dusk"], color="lightgrey", zorder=0)
            ax.axvspan(
                x["dusk"],
                x["midnight"] + datetime.timedelta(days=1),
                color="darkgrey",
                zorder=1
                )

        #zorder 1
        # grid
        ax.grid(axis="y", which="major", zorder=1, linewidth=0.1, color="k")
        ax.grid(axis="x", which="major", zorder=1, linewidth=0.1, color="k")

        #zorder 2
        #bars
        p1 = ax.bar(
            self.surf.index,
            self.surf["surf_max"],
            color=surf_colors["Hmax"],
            label="Hmax",
            zorder=2,
            width=0.1,
        )
        p2 = ax.bar(
            self.surf.index,
            self.surf["surf_min"],
            color=surf_colors["Hmin"],
            label="Hmin",
            zorder=3,
            width=0.1,
        )
        #zorder 3
        # now line
        ax.axvline(
            datetime.datetime.now(datetime.timezone.utc),
            color="r",
            label="Now",
            linewidth=0.5,
            zorder=3,
        )

        #zorder 4
        # labels
        # # barlabels
        ax.bar_label(
            p1,
            label_type="edge",
            zorder=4,
            size=5,
            fmt="%.1f",
            weight="bold",
            path_effects=[pe.withStroke(linewidth=1, foreground="w")],
        )
        ax.bar_label(
            p2,
            label_type="edge",
            zorder=4,
            size=5,
            fmt="%.1f",
            weight="bold",
            path_effects=[pe.withStroke(linewidth=1, foreground="w")],
        )
        # windspeed and wind direction colored on condition
        xs=self.surf.index.tolist()
        windspeeds=self.surf.speed.tolist()
        conditions=self.surf.directionType.tolist()
        winddirections=self.surf.direction.tolist()
        for x,ws,cond,wd in zip(xs,windspeeds,conditions,winddirections):
            ax.annotate(
                int(ws),
                xy=(mdates.date2num(x),hmax-(hmax*0.01)),
                fontsize=7,
                color=wind_colors[cond],
                zorder=4,
                weight="bold",
                va="top",
                ha="center",
                path_effects=[pe.withStroke(linewidth=1, foreground="w")],

            )
            ax.annotate(
                degToCompass(wd)+f"\n("+"{:.0f}".format(wd)+"°)",
                xy=(mdates.date2num(x),hmax-(hmax*0.04)),
                fontsize=4,
                color=wind_colors[cond],
                weight="bold",
                zorder=4,
                va="top",
                ha="center",
                path_effects=[pe.withStroke(linewidth=1, foreground="w")],

            )

        # dates index
        ax.figure.autofmt_xdate()
        ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=(0, 3, 6, 9, 12, 15, 18, 21)))
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.set(xlabel="Date (UTC Time)", ylabel="Surf Height [m]")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b"))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H"))

        # Rotates and right-aligns the x labels so they don't crowd each other.
        ax.tick_params(axis="x", which="major", pad=10)
        for label in ax.get_yticklabels(which="major"):
            label.set(rotation=0, size=4)
        for label in ax.get_xticklabels(which="major"):
            label.set(rotation=0, horizontalalignment="center", size=4)
        for label in ax.get_xticklabels(which="minor"):
            label.set(horizontalalignment="center", size=3)

        #lims
        ax.set_ylim([0, hmax])
        ax.set_xlim([self.surf.index[0], self.surf.index[-1]])

        #legend
        ax.legend(loc='lower left', bbox_to_anchor=(1, 0),fontsize=5)
        #windlegend 
        ax.annotate(
            "WIND",
            xy=(1.025,0.998),size=7,xycoords="axes fraction",va="top",ha="left"
        )
        ax.annotate(
            "Offshore",
            xy=(1.025,0.965),size=4,xycoords="axes fraction",va="top",ha="left",color=wind_colors["Offshore"]
        )
        ax.annotate(
            "Cross-shore",
            xy=(1.025,0.95),size=4,xycoords="axes fraction",va="top",ha="left",color=wind_colors["Cross-shore"]
        )
        ax.annotate(
            "Onshore",
            xy=(1.025,0.935),size=4,xycoords="axes fraction",va="top",ha="left",color=wind_colors["Onshore"]
        )
        f.set_tight_layout(True)
        return f

