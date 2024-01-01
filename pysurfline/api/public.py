"""api functions and classes"""

from .client import SurflineClient
from ..core import SpotForecasts

# from .models import SpotForecasts


def get_spot_forecasts(
    spotId: str, intervalHours: int = 3, days: int = 5
) -> SpotForecasts:
    """get spot forecast

    Get forecast for given spot by passing the spotId
    argument.

    Arguments:
        spotId (str): spot id
        intervalHours (int, optional): interval hours. Defaults to None.
        days (int, optional): days. Defaults to None.

    Returns:
        forecast (:obj:`SpotForecast`)
    """
    return SurflineClient().get_spot_forecasts(
        spotId, intervalHours=intervalHours, days=days
    )
