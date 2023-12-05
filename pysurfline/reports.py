"""reports"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import matplotlib.patheffects as pe

from pysurfline.core import SpotForecasts

SURF_COLORS = {"surf_max": "dodgerblue", "surf_min": "lightblue"}


class SurfReport:
    f: plt.Figure
    ax: plt.Axes
    forecasts: pd.DataFrame
    sunrisesunsettimes: pd.DataFrame

    def __init__(self, spotforecast: SpotForecasts):
        # spot name
        self.spot_name = spotforecast.name
        # data as dataframe
        self.forecasts = spotforecast.get_dataframe("forecasts")
        self.sunrisesunsettimes = spotforecast.get_dataframe("sunriseSunsetTimes")
        # figure
        self.f, self.ax = plt.subplots(dpi=300)
        pass

    @property
    def h_scale(self):
        # scale parameter
        factor = self.forecasts["surf_max"].max() * 1.2
        if factor < 2:
            factor = 2
        return factor

    def plot(self, barLabels: bool = False):
        """plot surf report

        Args:
            barLabels (bool, optional): surf height labels.
             Defaults to False.
        """
        # zorder 0 : night and day
        self._plot_daylight()

        # zorder 1 : grid
        self._plot_gird()

        # zorder 2,3 : bars (surf) and nowline
        barplots = self._plot_surf()
        self._plot_now_line()

        if barLabels:
            # zorder 4 : bar labels
            self._plot_bar_labels(barplots)

        # format axes
        self._fmt_ax()

        # title
        self.ax.set_title(self.spot_name)

        # legend
        self.ax.legend(loc="lower left", bbox_to_anchor=(1, 0), fontsize=5)
        # tight layout
        self.f.set_tight_layout(True)

    def _plot_gird(self):
        # zorder 1
        # grid
        self.ax.grid(axis="y", which="major", zorder=1, linewidth=0.1, color="k")
        self.ax.grid(axis="x", which="major", zorder=1, linewidth=0.1, color="k")

    def _plot_surf(self) -> tuple:
        """plot surf as bars"""
        # zorder 2 and 3
        barplots = []
        for i, ii in zip(["surf_max", "surf_min"], [2, 3]):
            barplots.append(
                self.ax.bar(
                    self.forecasts["timestamp_dt"],
                    self.forecasts[i],
                    color=SURF_COLORS[i],
                    label=i,
                    zorder=ii,
                    width=0.1,
                )
            )
        return barplots

    def _plot_now_line(self):
        # zorder 3
        # now line
        self.ax.axvline(
            datetime.datetime.now(datetime.timezone.utc),
            color="r",
            label="Now",
            linewidth=0.5,
            zorder=3,
        )

    def _fmt_ax(self):
        """ "fmt axes"""
        # dates index
        self.ax.figure.autofmt_xdate()
        self.ax.xaxis.set_minor_locator(
            mdates.HourLocator(byhour=(0, 3, 6, 9, 12, 15, 18, 21))
        )
        self.ax.xaxis.set_major_locator(mdates.DayLocator())
        self.ax.set(xlabel="Date (UTC Time)", ylabel="Surf Height [m]")
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b"))
        self.ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H"))

        # Rotates and right-aligns the x labels so they don't crowd each other.
        self.ax.tick_params(axis="x", which="major", pad=10)
        for label in self.ax.get_yticklabels(which="major"):
            label.set(rotation=0, size=4)
        for label in self.ax.get_xticklabels(which="major"):
            label.set(rotation=0, horizontalalignment="center", size=4)
        for label in self.ax.get_xticklabels(which="minor"):
            label.set(horizontalalignment="center", size=3)

        # lims
        self.ax.set_ylim([0, self.h_scale])
        self.ax.set_xlim(
            [
                self.forecasts["timestamp_dt"].iloc[0],
                self.forecasts["timestamp_dt"].iloc[-1],
            ]
        )

    def _plot_daylight(self):
        # zorder 0
        # night and day
        for i, x in self.sunrisesunsettimes.iterrows():
            self.ax.axvspan(
                x["midnight_dt"], x["sunrise_dt"], color="darkgrey", zorder=0
            )
            self.ax.axvspan(
                x["sunset_dt"],
                x["midnight_dt"] + datetime.timedelta(days=1),
                color="darkgrey",
                zorder=1,
            )

    def _plot_bar_labels(self, barplots: list):
        # zorder 4 barlabels
        for barplot in barplots:
            self.ax.bar_label(
                barplot,
                label_type="edge",
                zorder=4,
                size=5,
                fmt="%.1f",
                weight="bold",
                path_effects=[pe.withStroke(linewidth=1, foreground="w")],
            )


def plot_surf_report(spotforecast: SpotForecasts, **kwargs) -> SurfReport:
    """
    Plot surf report from a spotforecast object.

    Control the plot by passing a keyword arguments:
    - barLabels: label surf with height.

    Args:
        spotforecast (SpotForecast): SpotForecast object
        \\*\\*kwargs: Keyword arguments to pass to `SurfReport.plot`.

    Returns:
        SurfReport: SurfReport object
    """
    return SurfReport(spotforecast).plot(**kwargs)

    # def _plot_wind(self):
    #     # windspeed and wind direction colored on condition
    #     xs = self.forecasts.index.tolist()
    #     windspeeds = self.forecasts.speed.tolist()
    #     conditions = self.forecasts.directionType.tolist()
    #     winddirections = self.forecasts.direction.tolist()
    #     for x, ws, cond, wd in zip(xs, windspeeds, conditions, winddirections):
    #         ax.annotate(
    #             int(ws),
    #             xy=(mdates.date2num(x), h_scale - (h_scale * 0.01)),
    #             fontsize=7,
    #             color=wind_colors[cond],
    #             zorder=4,
    #             weight="bold",
    #             va="top",
    #             ha="center",
    #             path_effects=[pe.withStroke(linewidth=1, foreground="w")],
    #         )
    #         ax.annotate(
    #             degToCompass(wd) + "\n(" + "{:.0f}".format(wd) + "°)",
    #             xy=(mdates.date2num(x), h_scale - (h_scale * 0.04)),
    #             fontsize=4,
    #             color=wind_colors[cond],s
    #             weight="bold",
    #             zorder=4,
    #             va="top",
    #             ha="center",
    #             path_effects=[pe.withStroke(linewidth=1, foreground="w")],
    #         )
