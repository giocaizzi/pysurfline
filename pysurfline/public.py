from pysurfline.api.client import SurflineClient
from .core import SpotForecasts
from .reports.artist import SurfReport


def plot_surf_report(
    spotforecast: SpotForecasts, barLabels=False, wind=False, tides=False
) -> SurfReport:
    """
    Plot surf report from a spotforecast object.

    Args:
        spotforecast (SpotForecast): SpotForecast object
        barLabels (bool): label surf with height. Defaults to False.
        tide(bool):: plot tide height. Defaults to False.

    Returns:
        SurfReport: SurfReport object
    """
    return SurfReport(spotforecast).plot(barLabels=barLabels, wind=wind, tides=tides)


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
