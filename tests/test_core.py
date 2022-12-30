"""
test core classes.
"""
import pytest

from pysurfline import URLBuilder


def test_URLBuilder():
    params = {"spotId": "5842041f4e65fad6a7708890"}
    u = URLBuilder(type="wave", params=params)
    assert (
        u.url
        == "https://services.surfline.com/kbyg/spots/forecasts/wave?spotId=5842041f4e65fad6a7708890"
    )
