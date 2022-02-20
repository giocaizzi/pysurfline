"""
utility functions
"""

import collections


def flatten(d, parent_key="", sep="_"):
    """
    flatten nested dictionary, preserving lists

    Arguments:
        parent_key (str):
        sep (str):
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if v and isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def degToCompass(num):
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
