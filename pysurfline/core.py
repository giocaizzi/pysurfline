"""core module: SpotForecast"""

import pandas as pd

from .utils import flatten
from .api.objects import (
    SpotDetails,
    SpotForecastsWave,
    SpotForecastsWind,
    SpotForecastsTides,
    SpotForecastsSunlightTimes,
    SpotForecastsWeather,
)


class SpotForecasts:
    """spot forecasts data model

    Composite data model of all the spot forecasts data,
    - wave
    - condition (TODO)
    - wind
    - tides
    - weather and sunrise and sunset times

    TODO: add associated data and improve utcOffset
    """

    name: str = None

    def __init__(
        self,
        spotId: str,
        details: SpotDetails,
        waves: SpotForecastsWave,
        winds: SpotForecastsWind,
        tides: SpotForecastsTides,
        sunlightTimes: SpotForecastsSunlightTimes,
        weather: SpotForecastsWeather,
    ):
        self.spotId = spotId
        self.name = details.spot["name"]
        self.waves = waves.data
        self.wind = winds.data
        self.tides = tides.data
        self.weather = weather.data
        self.sunlightTimes = sunlightTimes.data

    def get_dataframe(self, attr="surf") -> pd.DataFrame:
        """pandas dataframe of selected attribute

        Use default to get the pandas dataframe of surf data,
        or of the selected attribute `attr`:
        - waves
        - wind
        - tides
        - weather
        - sunlightTimes

        Args:
            attr (str, optional): attribute to get dataframe from.
                Defaults to "surf".

        Raises:
            ValueError: if attr is not a valid attribute
        """
        if attr == "surf":
            # concat all dataframes
            data = []
            for attr in ["waves", "wind", "weather"]:
                # excluding "sunlightTimes" and "tides" due to different timestamps
                # TODO: include "surf" in `surf` output
                data.append(
                    pd.DataFrame(_flatten_objects(getattr(self, attr)))
                    .set_index("timestamp_dt")
                    .reset_index()
                )
            df = pd.concat(data, axis=1)
            # remove duplicated columns
            df = df.loc[:, ~df.columns.duplicated()]
            return df
        elif attr in ["waves", "wind", "tides", "weather", "sunlightTimes"]:
            # return single
            return pd.DataFrame(_flatten_objects(getattr(self, attr))).reset_index()
        else:
            raise ValueError(f"Attribute {attr} not supported. Use a valid attribute.")


def _flatten_objects(list_of_objects) -> list:
    """return list of flattened objects"""
    return [flatten(item.__dict__) for item in list_of_objects]
