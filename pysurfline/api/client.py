from pysurfline.api.services import ApiService
from pysurfline.core import SpotForecasts


class SurflineClient:
    """surfline client

    Surfline API client.
    At the moment, does not require authentication.

    TODO: Login and authentication
    """

    _baseurl: str = "https://services.surfline.com/kbyg/"

    def get_spot_forecasts(
        self, spotId: str, intervalHours: int = None, days: int = None
    ) -> SpotForecasts:
        """create a SpotForecast object from API responses

        Arguments:
            spotId (str): spot id
            intervalHours (int, optional): interval hours. Defaults to None.
            days (int, optional): days. Defaults to None.

        Returns:
            SpotForecast: SpotForecast object
        """
        params = {}
        params["spotId"] = spotId

        # add optional parameters
        if intervalHours:
            params["intervalHours"] = intervalHours
        if days:
            params["days"] = days

        return SpotForecasts(
            spotId,
            # spot datails are integrated with forecast,
            # hence the different GET args
            details=ApiService(self, "spots/details").get({"spotId": spotId}),
            waves=ApiService(self, "spots/forecasts/wave").get(params=params),
            winds=ApiService(self, "spots/forecasts/wind").get(params=params),
            tides=ApiService(self, "spots/forecasts/tides").get(params=params),
            # weather and sunlight times are in the same response
            weather=ApiService(self, "spots/forecasts/weather").get(params=params)[0],
            sunlightTimes=ApiService(self, "spots/forecasts/weather").get(
                params=params
            )[1],
        )
