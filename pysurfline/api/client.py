from pysurfline.api.services import ApiService
from pysurfline.api.objects import SpotForecasts


class SurflineClient:
    """surfline client

    Surfline API client.
    At the moment, does not require authentication.

    TODO Login and authentication
    """

    _baseurl: str = "https://services.surfline.com/kbyg/"

    def _get_spot_forecasts(self, spotId: str, **kwargs) -> SpotForecasts:
        """create a SpotForecast object from API responses

        Arguments:
            spotId (str): spot id
            \\*\\*kwargs: keyword arguments to spot/forecasts endpoint

        Returns:
            SpotForecast: SpotForecast object
        """
        kwargs["spotId"] = spotId
        return SpotForecasts(
            spotId,
            details=ApiService(self, "spots/details").get({"spotId": spotId}),
            waves=ApiService(self, "spots/forecasts/wave").get(params=kwargs),
            winds=ApiService(self, "spots/forecasts/wind").get(params=kwargs),
            tides=ApiService(self, "spots/forecasts/tides").get(
                params=kwargs
            ),
            weather=ApiService(self, "spots/forecasts/weather").get(
                params=kwargs
            )[0],
            sunlightTimes=ApiService(
                self, "spots/forecasts/weather"
            ).get(params=kwargs)[1],
        )
