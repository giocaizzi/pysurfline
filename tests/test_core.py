"""
test core classes.
"""
import pytest

from pysurfline import ForecastGetter

SPOTID = "5842041f4e65fad6a7708cfd"

@pytest.mark.parametrize("forecasttype",["wave","wind","tides","weather"])
def test_ForecastGetter_basic_request_URL(forecasttype):
    """test basic request URL"""
    f = ForecastGetter(forecasttype, params={"spotId": SPOTID})
    assert f.type == forecasttype
    assert (
        f.url == "https://services.surfline.com/kbyg/spots/forecasts/"\
        f"{forecasttype}"\
        f"?spotId={SPOTID}"
    )
    assert f.response.status_code == 200
