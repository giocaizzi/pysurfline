"""
test core classes.
"""
import pytest

from pysurfline import ForecastGetter

SPOTID = "5842041f4e65fad6a7708890"


def test_ForecastGetter():
    f = ForecastGetter("wave", params={"SpotId": SPOTID})
    assert f.type == "wave"
    assert (
        f.response.url == "https://services.surfline.com/kbyg/spots/forecasts/"
        "wave?SpotId=5842041f4e65fad6a7708890"
    )
