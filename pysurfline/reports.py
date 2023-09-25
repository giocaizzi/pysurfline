"""reports"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import matplotlib.patheffects as pe
from typing import Union, List
from pysurfline.models import SpotForecasts

SURF_COLORS = {"surf_max": "dodgerblue", "surf_min": "lightblue"}


def _plot_gird(ax: plt.Axes):
    # zorder 1
    # grid
    ax.grid(axis="y", which="major", zorder=1, linewidth=0.1, color="k")
    ax.grid(axis="x", which="major", zorder=1, linewidth=0.1, color="k")


def _plot_surf(spotforecasts: SpotForecasts, ax: plt.Axes) -> tuple:
    """plot surf as bars"""
    # zorder 2 and 3
    barplots = []
    for i, ii in zip(["surf_max", "surf_min"], [2, 3]):
        barplots.append(
            ax.bar(
                spotforecasts.get_dataframe("forecasts")["timestamp_dt"],
                spotforecasts.get_dataframe("forecasts")[i],
                color=SURF_COLORS[i],
                label=i,
                zorder=ii,
                width=0.1,
            )
        )
    return barplots


def _plot_now_line(ax: plt.Axes):
    # zorder 3
    # now line
    ax.axvline(
        datetime.datetime.now(datetime.timezone.utc),
        color="r",
        label="Now",
        linewidth=0.5,
        zorder=3,
    )


def _fmt_ax(spotforecasts: SpotForecasts, ax: plt.Axes, h_scale: float):
    """ "fmt axes"""
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

    # lims
    ax.set_ylim([0, h_scale])
    ax.set_xlim(
        [
            spotforecasts.get_dataframe("forecasts")["timestamp_dt"].iloc[0],
            spotforecasts.get_dataframe("forecasts")["timestamp_dt"].iloc[-1],
        ]
    )


def _plot_daylight(spotforecasts: SpotForecasts, ax: plt.Axes):
    # zorder 0
    # night and day
    for i, x in spotforecasts.get_dataframe("sunriseSunsetTimes").iterrows():
        ax.axvspan(
            x["midnight_dt"], x["sunrise_dt"], color="darkgrey", zorder=0
        )
        ax.axvspan(
            x["sunset_dt"],
            x["midnight_dt"] + datetime.timedelta(days=1),
            color="darkgrey",
            zorder=1,
        )


def _plot_bar_labels(barplots: list, ax: plt.Axes):
    # zorder 4 barlabels
    for barplot in barplots:
        ax.bar_label(
            barplot,
            label_type="edge",
            zorder=4,
            size=5,
            fmt="%.1f",
            weight="bold",
            path_effects=[pe.withStroke(linewidth=1, foreground="w")],
        )

def _plot_tides(spotforecasts: SpotForecasts, ax: plt.Axes):
    ax2 = ax.twinx()
    ax2.plot(
        spotforecasts.get_dataframe("tides")["timestamp_dt"],
        spotforecasts.get_dataframe("tides")["height"],
        color="k",
        linewidth=0.5,
        zorder=5,
    )
    ax2.set_position([0.1, 0.1, 0.8, 0.2])
    ax2.spines['bottom'].set_visible(False)
    ax2.tick_params(axis='x', which='both', length=0)


class AxisArtist:
    """AxisArtist

    This class is used to plot the surf report of a spot
    on a single matplotlib `plt.Axes` object.

    Args:
        spotforecasts (SpotForecasts): SpotForecasts object
        ax (plt.Axes): matplotlib axes object
        h_scale (Union[None, float], optional): scale parameter.
            Defaults to None.
    """

    _h_scale: float = 2.0

    def __init__(
        self,
        spotforecasts: SpotForecasts,
        ax: plt.Axes,
        h_scale: Union[None, float] = None,
    ):
        self.spotforecasts = spotforecasts
        # axes
        self.ax = ax

        # scale parameter
        # set to surf_max max * 1.2
        if (
            self.spotforecasts.get_dataframe("forecasts")["surf_max"].max()
            * 1.2
        ) > 2 and h_scale is None:
            self._h_scale = (
                self.spotforecasts.get_dataframe("forecasts")["surf_max"].max()
                * 1.2
            )
        elif h_scale is not None:
            self.h_scale = h_scale

    @property
    def h_scale(self):
        # scale parameter
        return self._h_scale

    @h_scale.setter
    def h_scale(self, value):
        self._h_scale = value

    def plot(self, barLabels: bool = False, tides: bool = False):
        # zorder 0 : night and day
        _plot_daylight(self.spotforecasts, self.ax)

        # zorder 1 : grid
        _plot_gird(self.ax)

        # zorder 2,3 : bars (surf) and nowline
        barplots = _plot_surf(self.spotforecasts, self.ax)
        _plot_now_line(self.ax)

        if barLabels:
            # zorder 4 : bar labels
            _plot_bar_labels(barplots, self.ax)

        if tides:
            _plot_tides(self.spotforecasts, self.ax)

        # format axes
        _fmt_ax(self.spotforecasts, self.ax, self.h_scale)

        # title
        self.ax.set_title(self.spotforecasts.name)

        # legend
        self.ax.legend(loc="lower left", bbox_to_anchor=(1, 0), fontsize=5)


class SurfReport:
    f: plt.Figure
    ax: Union[plt.Axes, List[plt.Axes]]
    _artists: List[AxisArtist] = []

    def __init__(
        self, spotforecasts: Union[SpotForecasts, List[SpotForecasts]], ncols=2
    ):
        if isinstance(spotforecasts, SpotForecasts):
            spotforecasts = [spotforecasts]
        self.spotforecasts = spotforecasts

        if len(spotforecasts) == 1:
            # axes
            self.f, self.ax = plt.subplots(dpi=300)
        else:
            # axes
            nrows = (
                len(spotforecasts) // ncols
                if len(spotforecasts) % 2 == 0
                else len(spotforecasts) // ncols + 1
            )
            self.f, self.ax = plt.subplots(ncols=ncols, nrows=nrows, dpi=300)

        # make ax a list of axes for single ax that would not be
        # so to be able to iterate over it
        self.ax = (
            np.array([self.ax]) if isinstance(self.ax, plt.Axes) else self.ax
        )

    def plot(
        self, barLabels: bool = False, tides: bool = False, sameScale: bool = False
    ) -> plt.Figure:
        """plot surf report

        Args:
            barLabels (bool, optional): surf height labels.
                Defaults to False.
            sameScale (bool, optional): same scale for all axes.

        Returns:
            plt.Figure: matplotlib figure
        """
        for isf, iax in zip(self.spotforecasts, self.ax.flatten()):
            self._artists.append(
                AxisArtist(isf, iax).plot(barLabels=barLabels, tides=tides)
            )

        self._delete_unnecessary_axis()

        # if samescale
        if sameScale:
            self._adjust_scale()

        # tight layout
        self.f.set_tight_layout(True)

        # close figure, it's returned
        plt.close()

        return self.f

    def _delete_unnecessary_axis(self):
        delAxes = None
        for i, iax in enumerate(self.ax.flatten()):
            if iax.has_data() is False:
                delAxes = i
        if delAxes is not None:
            self.f.delaxes(self.ax.flatten()[delAxes])
            # reset ax
            self.ax = self.f.get_axes()

    def _adjust_scale(self):
        h_scale = max([i.h_scale for i in self._artists])
        for iax in self.ax.flatten():
            iax.set_ylim([0, h_scale])


def plot_surf_report(spotforecasts: SpotForecasts, **kwargs) -> SurfReport:
    """
    Plot surf report from a spotforecasts object.

    Control the plot by passing a keyword arguments:
    - barLabels: label surf with height.
    - sameScale: same scale for all axes, if multiple axes are plotted.

    Args:
        spotforecasts (SpotForecast): SpotForecast object
        \\*\\*kwargs: Keyword arguments to pass to `SurfReport.plot`.

    Returns:
        SurfReport: SurfReport object
    """
    return SurfReport(spotforecasts).plot(**kwargs)

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
