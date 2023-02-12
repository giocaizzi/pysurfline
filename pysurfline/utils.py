"""
utility functions
"""
import sys

if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    from collections.abc import MutableMapping
else:
    from collections import MutableMapping


def flatten(d: dict, parent_key="", sep="_") -> dict:
    """
    flatten nested dictionary, preserving lists

    Arguments:
        parent_key (str): _
        sep (str): separator between upper and lowe level
            keys when concatenated in new key
    Returns:
        dict: flattened dictionary
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if v and isinstance(v, MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def degToCompass(num: float) -> str:
    """
    convert numerical (deg) direction into a cardinal string
    eg. N, S, W with a 22.5 deg accuracy.

    Args:
        num (float): angle in degrees

    Returns:
        str: cardinal string
    """
    val = int((num / 22.5) + 0.5)
    arr = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
    ]
    return arr[(val % 16)]
