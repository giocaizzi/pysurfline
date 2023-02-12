"""test utilis functions"""

import pytest

from pysurfline.utils import flatten, degToCompass


def test_flatten():
    """test flatten with default parameters"""
    d = {"k11": "surf", "k12": {"k21": "epic", "k22": "offshore"}}
    expected = {"k11": "surf", "k12_k21": "epic", "k12_k22": "offshore"}
    r = flatten(d)
    assert r == expected


@pytest.mark.parametrize("direction,expected", [(315, "NW"), (135, "SE"), (248, "WSW")])
def test_degToCompass(direction, expected):
    r = degToCompass(direction)
    assert r == expected
