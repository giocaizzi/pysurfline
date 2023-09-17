"""
utility functions
"""

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
