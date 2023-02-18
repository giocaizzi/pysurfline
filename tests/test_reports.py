"""test reports"""
import pytest
from pysurfline.core import SurflineAPI, SpotForecast
from pysurfline.reports import SurfReport
from unittest import mock
import pandas as pd


SPOT_ID = "123"


@pytest.fixture
@mock.patch("pysurfline.SurflineAPI.get_forecast")
def pacthed_SpotForecast(mock_get, cached_json):
    """return patched spotforecast"""
    mock_get.return_value = cached_json
    s = SpotForecast(SPOT_ID)
    s.load_forecast()
    return s

@pytest.fixture
@mock.patch("pysurfline.SurflineAPI.get_forecast")
def pacthed_SpotForecast_noinfo(mock_get, cached_json):
    """return patched spotforecast without having fetched data"""
    mock_get.return_value = cached_json
    s = SpotForecast(SPOT_ID)
    return s



def test_SurfReport_init(pacthed_SpotForecast):
    r = SurfReport(pacthed_SpotForecast)
    assert hasattr(r,"spotforecast")
    assert isinstance(r.spotforecast.forecasts,pd.DataFrame)

def test_SurfReport_init_missinginfo(pacthed_SpotForecast_noinfo):
    with pytest.raises(ValueError):
        SurfReport(pacthed_SpotForecast_noinfo)
