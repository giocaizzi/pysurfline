import pytest
import requests
from unittest import mock
from pysurfline.core import SurflineAPI, SpotForecast
import pandas as pd

SPOT_ID = "123"
ENDPOINT = "https://services.surfline.com/kbyg/spots/forecasts?"

################################################# SURFLINE API WRAPPER


@pytest.fixture
def api():
    return SurflineAPI(SPOT_ID)


def test_SurflineAPI_init(api):
    """
    Test the initialization of the API object.
    """
    assert api.endpoint == ENDPOINT
    assert api.spot_id == SPOT_ID


@mock.patch("pysurfline.core.requests.get")
def test_SurflineAPI_get_forecast(mock_get, api):
    """
    Test the retrieval of forecast data from the API.
    Both with default and custom parameters
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"foo": "bar"}

    # dafault parameters
    assert api.get_forecast() == {"foo": "bar"}
    mock_get.assert_called_once_with(
        f"{api.endpoint}",
        params={"spotId": SPOT_ID, "days": 3, "type": "surf", "interval_hours": 3},
    )

    # custom
    assert api.get_forecast(7, 6) == {"foo": "bar"}
    mock_get.assert_called_with(
        f"{api.endpoint}",
        params={"spotId": SPOT_ID, "days": 7, "type": "surf", "interval_hours": 6},
    )


@mock.patch("pysurfline.core.requests.get")
def test_SurflineAPI_get_forecast_error(mock_get, api):
    """
    Test the retrieval of forecast data from the API with an HTTP error status code.
    """
    mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError()

    with pytest.raises(requests.exceptions.HTTPError):
        api.get_forecast()


@mock.patch("pysurfline.core.requests.get")
def test_SurflineAPI_get_forecast_raises_othererror(mock_get, api):
    """
    Tests the retrieval of forecast data from the API with other errors.
    """
    mock_get.return_value.raise_for_status.side_effect = ValueError()
    with pytest.raises(ValueError):
        api.get_forecast()


################################################# CUSTOM CLASSES


@pytest.fixture
def spotforecast():
    return SpotForecast(SPOT_ID)

def test_SpotForecast_init(spotforecast):
    """
    Test the initialization of the SpotForecast object.
    """
    assert spotforecast.spot_id == SPOT_ID


@mock.patch("pysurfline.SurflineAPI.get_forecast")
def test_SpotForecast_load_forecast(mock_get, spotforecast,cached_json):
    mock_get.return_value = cached_json
    spotforecast.load_forecast()
    attrs = ["sunriseSunsetTimes", "tideLocation", "forecasts", "tides"]
    for attr in attrs:
        assert hasattr(spotforecast, attr)
        assert isinstance(getattr(spotforecast, attr), pd.DataFrame)
