"""reports"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from pysurfline.utils import degToCompass
import numpy as np
import matplotlib.patheffects as pe
from pysurfline import SpotForecast


class SurfReport(SpotForecast):
    """
    Structured spot surf-report object.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._set_df()
        self._get_simple_surf_report()

    def _set_df(self):
        df = []
        for attr in [
            "wave",
            "wind",
            "weather",
        ]:  # exclude "tides" because of HIGH LOW exact times
            df.append(self.get_dataframe(attr))
        df = pd.concat(df, axis=1)
        self.df = df

    def _get_simple_surf_report(self):
        self.surf = self.df.copy()[
            ["surf_min", "surf_max", "speed", "directionType", "direction"]
        ]
        # set Hmin <0.2m to nan for plotting reasons
        self.surf.loc[(self.df["surf_min"] < 0.2), "surf_min"] = np.nan

    def plot(self):
        f, ax = plt.subplots(dpi=300)
        surf_colors = {"Hmax": "dodgerblue", "Hmin": "lightblue"}
        wind_colors = {
            "Cross-shore": "coral",
            "Offshore": "green",
            "Onshore": "darkred",
        }
        daylight = self.get_dataframe("sunlightTimes")

        # scale parameter
        hmax = self.surf["surf_max"].max()
        hmax = hmax * 1.2
        if hmax < 2:
            hmax = 2

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
                zorder=1,
            )

        # zorder 1
        # grid
        ax.grid(axis="y", which="major", zorder=1, linewidth=0.1, color="k")
        ax.grid(axis="x", which="major", zorder=1, linewidth=0.1, color="k")

        # zorder 2
        # bars
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
        # zorder 3
        # now line
        ax.axvline(
            datetime.datetime.now(datetime.timezone.utc),
            color="r",
            label="Now",
            linewidth=0.5,
            zorder=3,
        )

        # zorder 4
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
        xs = self.surf.index.tolist()
        windspeeds = self.surf.speed.tolist()
        conditions = self.surf.directionType.tolist()
        winddirections = self.surf.direction.tolist()
        for x, ws, cond, wd in zip(xs, windspeeds, conditions, winddirections):
            ax.annotate(
                int(ws),
                xy=(mdates.date2num(x), hmax - (hmax * 0.01)),
                fontsize=7,
                color=wind_colors[cond],
                zorder=4,
                weight="bold",
                va="top",
                ha="center",
                path_effects=[pe.withStroke(linewidth=1, foreground="w")],
            )
            ax.annotate(
                degToCompass(wd) + "\n(" + "{:.0f}".format(wd) + "°)",
                xy=(mdates.date2num(x), hmax - (hmax * 0.04)),
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
        ax.set_ylim([0, hmax])
        ax.set_xlim([self.surf.index[0], self.surf.index[-1]])

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
            color=wind_colors["Offshore"],
        )
        ax.annotate(
            "Cross-shore",
            xy=(1.025, 0.95),
            size=4,
            xycoords="axes fraction",
            va="top",
            ha="left",
            color=wind_colors["Cross-shore"],
        )
        ax.annotate(
            "Onshore",
            xy=(1.025, 0.935),
            size=4,
            xycoords="axes fraction",
            va="top",
            ha="left",
            color=wind_colors["Onshore"],
        )
        f.set_tight_layout(True)
        return f
