"""api functions and classes"""

import requests

# from .models import SpotForecasts


# def get_spot_forecasts(spotId: str,**kwargs) -> SpotForecasts:
#     """get spot forecast

#     Get forecast for given spot by passing the spotId
#     argument.

#     Arguments:
#         spotId (str): spot id

#     Returns:
#         forecast (:obj:`SpotForecast`)
#     """
#     return SurflineClient()._get_spot_forecasts(spotId,**kwargs)


class SurflineClient:
    """surfline client

    Surfline API client.
    At the moment, does not require authentication.
    """

    _baseurl: str = "https://services.surfline.com/kbyg/"

#     def _get_spot_forecasts(self, spotId: str, **kwargs) -> SpotForecasts:
#         """create a SpotForecast object from API responses

#         Arguments:
#             spotId (str): spot id
#             \\*\\*kwargs: keyword arguments to spot/forecasts endpoint

#         Returns:
#             SpotForecast: SpotForecast object
#         """
#         kwargs["spotId"] = spotId
#         return SpotForecasts(
#             spotId,
#             **APIResource(self, "spots/details")
#             .get(params={"spotId": spotId})
#             .json["spot"],
#             **APIResource(self, "spots/forecasts")
#             .get(params=kwargs)
#             .json["data"],
#         )
