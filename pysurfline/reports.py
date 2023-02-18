"""reports"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np
import matplotlib.patheffects as pe
from pysurfline.utils import degToCompass
from pysurfline import SpotForecast


SURF_COLORS = {"Hmax": "dodgerblue", "Hmin": "lightblue"}
WIND_COLORS = {"Cross-shore": "coral", "Offshore": "green", "Onshore": "darkred"}


class SurfReport:
    """
    Structured spot surf-report object.
    """

    def __init__(self, spotforecast: SpotForecast):
        if hasattr(spotforecast, "forecasts"):
            self.spotforecast = spotforecast
        else:
            raise ValueError("SpotForecast object must have a `forecast` attribute")

    def plot(self):
        f, ax = plt.subplots(dpi=300)

        self._add_day_night(ax)
        self._add_grid(ax)
        self._add_bars(ax)
        self._add_now_line(ax)
        self._add_labels(ax)
        self._add_dates(ax)

        plt.show()

    def _add_day_night(self, ax):
        daylight = self.spotforecast.sunriseSunsetTimes

        for i, x in daylight.iterrows():
            ax.axvspan(x["midnight"], x["sunrise"], color="darkgrey", zorder=0)
            ax.axvspan(
                x["sunset"],
                x["midnight"] + datetime.timedelta(days=1),
                color="darkgrey",
                zorder=1,
            )

    def _add_grid(self, ax):
        ax.grid(axis="y", which="major", zorder=1, linewidth=0.1, color="k")
        ax.grid(axis="x", which="major", zorder=1, linewidth=0.1, color="k")

    def _add_bars(self, ax):
        hmax = self.forecasts["surf.max"].max() * 1.2
        if hmax < 2:
            hmax = 2

        p1 = ax.bar(
            self.forecasts.index,
            self.forecasts["surf.max"],
            color=SURF_COLORS["Hmax"],
            label="Hmax",
            zorder=2,
            width=0.1,
        )
        p2 = ax.bar(
            self.forecasts.index,
            self.forecasts["surf.min"],
            color=SURF_COLORS["Hmin"],
            label="Hmin",
            zorder=3,
            width=0.1,
        )

        self.bars = [p1, p2]
        self.hmax = hmax

    def _add_now_line(self, ax):
        ax.axvline(
            datetime.datetime.now(datetime.timezone.utc),
            color="r",
            label="Now",
            linewidth=0.5,
            zorder=3,
        )

    def _add_labels(self, ax):
        xs = self.forecasts.index.tolist()
        windspeeds = self.forecasts.speed.tolist()
        conditions = self.forecasts.directionType.tolist()
        winddirections = self.forecasts.direction.tolist()
        for x, ws, cond, wd in zip(xs, windspeeds, conditions, winddirections):
            ax.annotate(
                int(ws),
                xy=(mdates.date2num(x), self.hmax - (self.hmax * 0.01)),
                fontsize=7,
                color=WIND_COLORS[cond],
                zorder=4,
                weight="bold",)
               
