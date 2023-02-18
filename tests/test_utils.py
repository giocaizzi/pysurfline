"""test utilis functions"""

import pytest

from pysurfline.utils import degToCompass


@pytest.mark.parametrize("direction,expected", [(315, "NW"), (135, "SE"), (248, "WSW")])
def test_degToCompass(direction, expected):
    r = degToCompass(direction)
    assert r == expected
