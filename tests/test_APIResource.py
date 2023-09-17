# import pytest
# from pysurfline.api import SurflineClient, APIResource


# @pytest.fixture
# def surfline_client():
#     return SurflineClient()


# def test_get_spot_forecasts(surfline_client):
#     spot_id = "5842041f4e65fad6a7708e7a"
#     forecasts = surfline_client._get_spot_forecasts(spot_id)
#     assert forecasts.spot_id == spot_id


# def test_api_resource_get():
#     client = SurflineClient()
#     resource = APIResource(client, "spots/details")
#     response = resource.get(params={"spotId": "5842041f4e65fad6a7708e7a"})
#     assert response.status_code == 200
#     assert response.json["spot"]["name"] == "Malibu First Point"


# def test_api_resource_get_with_error():
#     client = SurflineClient()
#     resource = APIResource(client, "spots/details")
#     response = resource.get(params={"spotId": "invalid_id"})
#     assert response.status_code == 404
