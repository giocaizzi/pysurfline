import pytest
from unittest.mock import MagicMock, patch
import pytest
from requests.exceptions import HTTPError, ConnectionError, SSLError

from pysurfline.api import APIResource
from .test_models import TEST_API_RESPONSE_DATA

TEST_BASEURL = "test_baseurl/"
TEST_ENDPOINT = "test_endpoint"


@pytest.fixture
def mock_client():
    """Create a mock Client object

    As the only attribute required from client
    is the baseurl, we can mock the entire object.
    """
    mock_client = MagicMock()
    mock_client._baseurl = TEST_BASEURL
    return mock_client


def test_APIResource_init(mock_client):
    """Test APIResource initialization"""
    # Create an APIResource object
    api_resource = APIResource(mock_client, TEST_ENDPOINT)

    # Assert that the mocked client attribute was set correctly
    assert api_resource._client == mock_client
    # Assert that the endpoint attribute was set correctly
    assert api_resource._endpoint == TEST_ENDPOINT


def test_APIResource_get_200(mock_client):
    """Test APIResource get method"""
    # Create a mock response
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": TEST_API_RESPONSE_DATA}
    mock_response.status_code = 200
    mock_response.url = mock_client._baseurl + TEST_ENDPOINT

    # Set the mock response for the mock requests.get method
    mock_get = MagicMock(return_value=mock_response)
    with patch("pysurfline.api.requests.get", mock_get):
        # Create an APIResource object
        api_resource = APIResource(mock_client, TEST_ENDPOINT)
        # Call the get method and assert returns self
        assert api_resource.get() == api_resource
        # Assert that the response object was set correctly
        assert api_resource.response == mock_response
        # Assert that the url property returns the correct value
        assert api_resource.url == "test_baseurl/test_endpoint"
        # Assert that the json property returns the correct value
        assert api_resource.json == {"data": TEST_API_RESPONSE_DATA}
        # Assert that the status_code property returns the correct value
        assert api_resource.status_code == 200


def test_APIResource_get_HTTPError(mock_client):
    """Test APIResource get method with a generic HTTPError"""
    # Create a mock response that r
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError
    # Set the mock response for the mock requests.get method
    mock_get = MagicMock(return_value=mock_response)
    with patch("pysurfline.api.requests.get", mock_get):
        # Create an APIResource object
        api_resource = APIResource(mock_client, TEST_ENDPOINT)
        with pytest.raises(HTTPError):
            api_resource.get()


def test_APIResource_get_ConnectionError(mock_client):
    """Test APIResource get method with a generic ConnectionError"""
    # Create a mock response
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = ConnectionError
    # Set the mock response for the mock requests.get method
    mock_get = MagicMock(return_value=mock_response)
    with patch("pysurfline.api.requests.get", mock_get):
        # Create an APIResource object
        api_resource = APIResource(mock_client, TEST_ENDPOINT)
        with pytest.raises(ConnectionError):
            api_resource.get()


def test_APIResource_get_RequestException(mock_client):
    """Test APIResource get method with a generic RequestException"""
    # Create a mock response
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = SSLError
    # Set the mock response for the mock requests.get method
    mock_get = MagicMock(return_value=mock_response)
    with patch("pysurfline.api.requests.get", mock_get):
        # Create an APIResource object
        api_resource = APIResource(mock_client, TEST_ENDPOINT)
        with pytest.raises(SSLError):
            api_resource.get()
