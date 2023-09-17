"""
utility functions
"""
from collections import MutableMapping


from dataclasses import is_dataclass


def flatten_dict(d: dict, parent_key: str = "", sep: str = "_") -> dict:
    """
    Flatten a nested dictionary.

    Args:
        d (dict): dictionary to flatten
        parent_key (str): parent key
        sep (str): separator

    Returns:
        dict: flattened dictionary
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, MutableMapping):
                    items.extend(
                        flatten_dict(item, f"{new_key}{sep}{i}", sep=sep).items()
                    )
                elif is_dataclass(item):
                    items.extend(
                        flatten_dict(
                            item.__dict__, f"{new_key}{sep}{i}", sep=sep
                        ).items()
                    )
                else:
                    items.append((f"{new_key}{sep}{i}", item))
        elif is_dataclass(v):
            items.extend(flatten_dict(v.__dict__, new_key, sep=sep).items())
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
