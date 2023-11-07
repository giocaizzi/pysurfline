"""api functions and classes"""

from .client import SurflineClient
from .objects import SpotForecasts

# from .models import SpotForecasts


def get_spot_forecasts(spotId: str, **kwargs) -> SpotForecasts:
    """get spot forecast

    Get forecast for given spot by passing the spotId
    argument.

    Known keyword arguments are:
    - days (int): number of days to forecast
    - intervalHours (int): interval in hours between forecasts

    Arguments:
        spotId (str): spot id
        \\*\\*kwargs: keyword arguments to spot/forecasts endpoint

    Returns:
        forecast (:obj:`SpotForecast`)
    """
    return SurflineClient()._get_spot_forecasts(spotId, **kwargs)
