"""test reports"""
import pytest
from pysurfline.core import SurflineAPI, SpotForecast
from pysurfline.reports import SurfReport
from unittest import mock
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import datetime


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


def test_add_now_line(patched_SpotForecast):
    """test that a red line is placed at the now date"""
    r = SurfReport(patched_SpotForecast)
    now = matplotlib.dates.date2num(
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
        es1 = matplotlib.dates.date2num(expected_span[0])
        es2 = matplotlib.dates.date2num(expected_span[1])
        as1 = patch.get_xy()[0, 0]
        as2 = patch.get_xy()[3, 0]

        print(as1, as2, es1, es2)

        assert as1 == es1
        assert as2 == es2
