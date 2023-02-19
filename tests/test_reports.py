"""test reports"""
import pytest
from pysurfline.core import SpotForecast
from pysurfline.reports import SurfReport
from unittest import mock
import pandas as pd
from matplotlib.dates import date2num
import matplotlib.pyplot as plt
import datetime
import matplotlib
import matplotlib.patheffects as pe

# decorator from matplotlib.testing.decorators 
# to ensure that the figure is closed at the end of the test.


SPOT_ID = "123"


@pytest.fixture
@mock.patch("pysurfline.SurflineAPI.get_forecast")
def patched_SpotForecast(mock_get, cached_json):
    """return patched spotforecast"""
    mock_get.return_value = cached_json
    s = SpotForecast(SPOT_ID)
    s.load_forecast()
    return s


@pytest.fixture
@mock.patch("pysurfline.SurflineAPI.get_forecast")
def patched_SpotForecast_noinfo(mock_get, cached_json):
    """return patched spotforecast without having fetched data"""
    mock_get.return_value = cached_json
    s = SpotForecast(SPOT_ID)
    return s


def test_SurfReport_init(patched_SpotForecast):
    """test initailzation"""
    r = SurfReport(patched_SpotForecast)
    assert hasattr(r, "spotforecast")
    assert isinstance(r.spotforecast.forecasts, pd.DataFrame)


def test_SurfReport_init_missinginfo(patched_SpotForecast_noinfo):
    """test failed intialization with object that did not have forecast yet"""
    with pytest.raises(ValueError):
        SurfReport(patched_SpotForecast_noinfo)


def test_add_wave_labels(patched_SpotForecast):
    r = SurfReport(patched_SpotForecast)
    fig, ax = plt.subplots()
    r._add_bars(ax)
    r._add_wave_labels(ax)
    assert len(r.bars) == 2
    for ib,bardata in zip(r.bars,[patched_SpotForecast.forecasts["surf.max"],patched_SpotForecast.forecasts["surf.min"]]):
        labelcollection = ax.bar_label(ib)

        ## get_text() restitutes raw data, ignoring formatting
        assert labelcollection[0].get_text() == f"{bardata[0]}"
        assert labelcollection[0].get_fontsize() == 10
        # # assert labelcollection[0].get_fontweight() == "bold"
        # assert labelcollection[0].get_path_effects()[0].get_linewidth() == 1
        # assert labelcollection[0].get_path_effects()[0].get_foreground() == "w"

def test_add_grid(patched_SpotForecast):
    r = SurfReport(patched_SpotForecast)
    fig, ax = plt.subplots()
    r._add_grid(ax)
    ygridlines = ax.yaxis.get_gridlines()
    assert len(ygridlines) > 0
    for line in ygridlines:
        assert line.get_linewidth() == 0.1
        assert line.get_color() == "k"
    xgridlines = ax.xaxis.get_gridlines()
    assert len(xgridlines) > 0
    for line in xgridlines:
        assert line.get_linewidth() == 0.1
        assert line.get_color() == "k"


def test_add_bars(patched_SpotForecast):
    """test that a red line is placed at the now date"""
    r = SurfReport(patched_SpotForecast)    
    fig, ax = plt.subplots()
    r._add_bars(ax)
    
    patches = ax.get_children()
    actual_patches = [p for p in patches if isinstance(p, matplotlib.patches.Polygon)]

    assert len(ax.patches) == len(patched_SpotForecast.forecasts)*2

    # Check that the patches are located correctly
    for i, patch in enumerate(actual_patches):
        assert patch.get_width() == 0.1
        v1=patch.get_xy()[0, 0]
        v2=patch.get_xy()[3, 0]
        print(
            i,
            v1,
            v2
        )
        assert patch.get_x() == date2num(patched_SpotForecast.forecasts["timestamp"].iloc[i])


def test_add_now_line(patched_SpotForecast):
    """test that a red line is placed at the now date"""
    r = SurfReport(patched_SpotForecast)
    now = date2num(
        patched_SpotForecast.sunriseSunsetTimes["midnight"][0]
        + datetime.timedelta(hours=4)
    )
    fig, ax = plt.subplots()

    with mock.patch("pysurfline.reports.datetime.datetime") as mock_now:
        mock_now.now.return_value = now
        r._add_now_line(ax)

    # Check that the line exists and is in the correct position
    lines = ax.get_lines()
    assert len(lines) == 1
    assert lines[0].get_color() == "r"
    assert lines[0].get_linewidth() == 0.5
    assert lines[0].get_label() == "Now"
    assert lines[0].get_xdata() == pytest.approx([now, now], abs=1e-2)


def test_add_day_night(patched_SpotForecast):
    sunrise_sunset_times = patched_SpotForecast.sunriseSunsetTimes
    sunrise_sunset_times["endoftheday"] = sunrise_sunset_times[
        "midnight"
    ] + datetime.timedelta(days=1)
    expected = list(
        sunrise_sunset_times.unstack()
        .reset_index(drop=True)
        .sort_values()
        .reset_index(drop=True)
    )
    expected_spans = [
        (expected[i], expected[i + 1]) for i in range(len(expected)) if i % 2 == 0
    ]
    expected_colors = [
        (0.6627450980392157, 0.6627450980392157, 0.6627450980392157, 1.0)
    ]

    r = SurfReport(patched_SpotForecast)
    fig, ax = plt.subplots()
    r._add_day_night(ax)

    patches = ax.get_children()
    actual_patches = [p for p in patches if isinstance(p, matplotlib.patches.Polygon)]

    assert len(actual_patches) == len(sunrise_sunset_times) * 2
    assert len(actual_patches) == len(expected_spans)

    for patch, expected_span, expected_color in zip(
        actual_patches, expected_spans, expected_colors * len(expected_spans)
    ):
        assert patch.get_facecolor() == expected_color
        es1 = date2num(expected_span[0])
        es2 = date2num(expected_span[1])
        as1 = patch.get_xy()[0, 0]
        as2 = patch.get_xy()[3, 0]

        print(as1, as2, es1, es2)

        assert as1 == es1
        assert as2 == es2
