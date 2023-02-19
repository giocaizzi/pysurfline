"""reports"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
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
        f, ax = plt.subplots()

        self.hmax = self.spotforecast.forecasts["surf.max"].max() * 1.2
        if self.hmax < 2:
            self.hmax = 2

        self._set_xlims(ax)
        self._add_day_night(ax)
        self._add_grid(ax)
        self._add_bars(ax)
        self._add_now_line(ax)

        # self._add_labels(ax)
        # self._add_dates(ax)
        # self._add_legend(ax)

        plt.show()
    
    def _set_xlims(self,ax):
        """set xlims"""
        ax.set_ylim([0, self.hmax])
        ax.set_xlim(
            [
                self.spotforecast.forecasts["timestamp"].iloc[0],
                self.spotforecast.forecasts["timestamp"].iloc[-1],
            ]
        )

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
        p1 = ax.bar(
            self.spotforecast.forecasts["timestamp"],
            self.spotforecast.forecasts["surf.max"],
            color=SURF_COLORS["Hmax"],
            label="Hmax",
            zorder=2,
            width=0.1,
        )
        p2 = ax.bar(
            self.spotforecast.forecasts["timestamp"],
            self.spotforecast.forecasts["surf.min"],
            color=SURF_COLORS["Hmin"],
            label="Hmin",
            zorder=3,
            width=0.1,
        )

        self.bars = [p1, p2]

    def _add_now_line(self, ax):
        ax.axvline(
            datetime.datetime.now(datetime.timezone.utc),
            color="r",
            label="Now",
            linewidth=0.5,
            zorder=3,
        )

    def _add_labels(self, ax):
        ax.bar_label(
            self.bars[0],
            label_type="edge",
            zorder=4,
            size=5,
            fmt="%.1f",
            weight="bold",
            path_effects=[pe.withStroke(linewidth=1, foreground="w")],
        )
        ax.bar_label(
            self.bars[1],
            label_type="edge",
            zorder=4,
            size=5,
            fmt="%.1f",
            weight="bold",
            path_effects=[pe.withStroke(linewidth=1, foreground="w")],
        )
        # windspeed and wind direction colored on condition
        xs = self.spotforecast.forecasts.index.tolist()
        windspeeds = self.spotforecast.forecasts["wind.speed"].tolist()
        winddirections = self.spotforecast.forecasts["wind.direction"].tolist()
        for x, ws, wd in zip(xs, windspeeds, winddirections):
            ax.annotate(
                int(ws),
                xy=(mdates.date2num(x), self.hmax - (self.hmax * 0.01)),
                fontsize=7,
                color="k",
                zorder=4,
                weight="bold",
                va="top",
                ha="center",
                path_effects=[pe.withStroke(linewidth=1, foreground="w")],
            )
            ax.annotate(
                degToCompass(wd) + "\n(" + "{:.0f}".format(wd) + "°)",
                xy=(mdates.date2num(x), self.hmax - (self.hmax * 0.04)),
                fontsize=4,
                color="k",
                weight="bold",
                zorder=4,
                va="top",
                ha="center",
                path_effects=[pe.withStroke(linewidth=1, foreground="w")],
            )

    def _add_dates(self, ax):
        # dates index
        ax.figure.autofmt_xdate()
        ax.xaxis.set_minor_locator(
            mdates.HourLocator(byhour=(0, 3, 6, 9, 12, 15, 18, 21))
        )
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


    def _add_legend(self, ax):
        # legend
        ax.legend(loc="lower left", bbox_to_anchor=(1, 0), fontsize=5)
        # windlegend
        ax.annotate(
            "WIND",
            xy=(1.025, 0.998),
            size=7,
            xycoords="axes fraction",
            va="top",
            ha="left",
        )
        ax.annotate(
            "Offshore",
            xy=(1.025, 0.965),
            size=4,
            xycoords="axes fraction",
            va="top",
            ha="left",
            color=WIND_COLORS["Offshore"],
        )
        ax.annotate(
            "Cross-shore",
            xy=(1.025, 0.95),
            size=4,
            xycoords="axes fraction",
            va="top",
            ha="left",
            color=WIND_COLORS["Cross-shore"],
        )
        ax.annotate(
            "Onshore",
            xy=(1.025, 0.935),
            size=4,
            xycoords="axes fraction",
            va="top",
            ha="left",
            color=WIND_COLORS["Onshore"],
        )
