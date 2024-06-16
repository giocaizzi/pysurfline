"""api functions and classes"""

from ..core import SpotForecasts
from .client import SurflineClient

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
        forecast (`SpotForecast`)
    """
    return SurflineClient().get_spot_forecasts(
        spotId, intervalHours=intervalHours, days=days
    )
