import pytest
import requests
from unittest import mock
from pysurfline.core import SurflineAPI


@pytest.fixture
def api():
    return SurflineAPI("123")


def test_init(api):
    """
    Test the initialization of the API object.
    """
    assert api.endpoint == "https://services.surfline.com/kbyg/spots/forecasts?"
    assert api.spot_id == "123"


@mock.patch("pysurfline.core.requests.get")
def test_get_forecast(mock_get, api):
    """
    Test the retrieval of forecast data from the API.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"foo": "bar"}

    # dafault parameters
    assert api.get_forecast() == {"foo": "bar"}
    mock_get.assert_called_once_with(
        f"{api.endpoint}",
        params={"spotId": "123", "days": 3, "type": "surf", "interval_hours": 3},
    )

    # custom
    assert api.get_forecast("wind", 2, 6) == {"foo": "bar"}
    mock_get.assert_called_with(
        f"{api.endpoint}",
        params={"spotId": "123", "days": 2, "type": "wind", "interval_hours": 6},
    )


@mock.patch("pysurfline.core.requests.get")
def test_get_forecast_error(mock_get, api):
    """
    Test the retrieval of forecast data from the API with an error status code.
    """
    mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError()

    with pytest.raises(requests.exceptions.HTTPError):
        api.get_forecast()


@mock.patch("pysurfline.core.requests.get")
def test_get_forecast_raises_othererror(mock_get, api):
    mock_get.return_value.raise_for_status.side_effect = ValueError()

    with pytest.raises(ValueError):
        api.get_forecast()
