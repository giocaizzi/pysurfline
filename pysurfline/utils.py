"""
utility functions
"""
from collections.abc import MutableMapping
from dataclasses import is_dataclass

from .api.models.spots import Time


def flatten(d: dict, parent_key: str = "", sep: str = "_") -> dict:
    """
    Recursively flattens a nested dictionary.

    Args:
        d (dict): The dictionary to flatten.
        parent_key (str): The parent key to use for the flattened keys.
        sep (str): The separator to use between keys.

    Returns:
        dict: The flattened dictionary.
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, MutableMapping):
                    items.extend(flatten(item, f"{new_key}{sep}{i}", sep=sep).items())
                elif is_dataclass(item):
                    items.extend(
                        flatten(item.__dict__, f"{new_key}{sep}{i}", sep=sep).items()
                    )
                else:
                    items.append((f"{new_key}{sep}{i}", item))
        elif is_dataclass(v) or isinstance(v, Time):
            items.extend(flatten(v.__dict__, new_key, sep=sep).items())
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
