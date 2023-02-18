"""test reports"""
import pytest
from pysurfline.core import  SurflineAPI,SpotForecast
from unittest import mock


SPOT_ID="123"
@pytest.fixture
@mock.patch("pysurfline.SurflineAPI.get_forecast")
def pacthed_SpotForecast(mock_get,cached_json):
    mock_get.return_value = cached_json
    s = SpotForecast(SPOT_ID)
    s.load_forecast()
    return

def test_SurfReport_init():
    pass