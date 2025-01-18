"""Tests for the Initialize class and its helper classes."""

from unittest.mock import patch, AsyncMock, MagicMock
import pytest
from pytest import MonkeyPatch
import httpx
from src.brain._initialize import Initialize, Extract, Serialize

def _mock_response(json_data=None, status_code=200):
    """Return a mock response object."""
    mock_response = MagicMock()
    mock_response.json.return_value = json_data
    mock_response.status_code = status_code
    mock_response.raise_for_status.side_effect = None
    return mock_response

class TestInitialize:
    """Tests for the Initialize class."""

    @pytest.mark.asyncio
    async def test_load_bikes_successful(self):
        """Test that _load_bikes() loads bikes from the backend."""
        MonkeyPatch().setenv("BACKEND_URL", "http://localhost:8000")

        init = Initialize(token="token")
        init.bikes = None

        mock_bike_data = {
            "data": [
                {
                    "id": 5,
                    "attributes": {"last_position": "POINT(13.06782 55.577859)"}
                },
                {
                    "id": 7,
                    "attributes": {"last_position": "POINT(13.06783 55.577860)"}
                }
            ]
        }

        with patch("httpx.AsyncClient", autospec=True) as mock_client_class:
            mock_client_instance = MagicMock()
            mock_client_class.return_value.__aenter__.return_value = mock_client_instance
            mock_client_instance.get = AsyncMock(
                return_value=_mock_response(json_data=mock_bike_data))
            await init._load_bikes()
            assert init.bikes == mock_bike_data["data"]
            mock_client_instance.get.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_load_bikes_already_loaded(self):
        """Test that _load_bikes() does not reload bikes if they're already loaded."""
        init = Initialize(token="token")
        init.bikes = [{"bikes_already_loaded": 999}]
        with patch("httpx.AsyncClient", autospec=True) as mock_client_class:
            mock_client_instance = MagicMock()
            mock_client_class.return_value.__aenter__.return_value = mock_client_instance
            mock_client_instance.get = AsyncMock()
            await init._load_bikes()
            mock_client_instance.get.assert_not_awaited()
            assert init.bikes == [{"bikes_already_loaded": 999}]

    @pytest.mark.asyncio
    async def test_load_bikes_request_error(self):
        """Test that _load_bikes() raises a RequestError if the request fails."""
        MonkeyPatch().setenv("BACKEND_URL", "http://localhost:8000")
        init = Initialize(token="token")
        init.bikes = None
        with patch("httpx.AsyncClient", autospec=True) as mock_client_class:
            mock_client_instance = MagicMock()
            mock_client_class.return_value.__aenter__.return_value = mock_client_instance
            mock_client_instance.get.side_effect = httpx.RequestError("Connection failed")
            with pytest.raises(
                httpx.RequestError,
                match="Failed to request bikes: Connection failed"):
                await init._load_bikes()
            assert init.bikes is None

    @pytest.mark.asyncio
    async def test_bike_ids_calls_load_bikes(self):
        """Test that bike_ids() calls _load_bikes() and returns a serialized list of bike IDs."""
        MonkeyPatch().setenv("BACKEND_URL", "http://localhost:8000")
        init = Initialize(token="token")
        init.bikes = None

        mock_bike_data = {
            "data": [
                {
                    "id": 5,
                    "attributes": {"last_position": "POINT(11.11 22.22)"}
                },
                {
                    "id": 7,
                    "attributes": {"last_position": "POINT(33.33 44.44)"}
                }
            ]
        }

        with patch("httpx.AsyncClient", autospec=True) as mock_client_class:
            mock_client_instance = MagicMock()
            mock_client_class.return_value.__aenter__.return_value = mock_client_instance
            mock_client_instance.get = AsyncMock(
                return_value=_mock_response(json_data=mock_bike_data))
            result = await init.bike_ids()
            assert result == "5,7"
            assert init.bikes == mock_bike_data["data"]

    @pytest.mark.asyncio
    async def test_bike_positions(self):
        """Test that bike_positions() calls _load_bikes() and 
        returns a serialized list of bike positions."""
        MonkeyPatch().setenv("BACKEND_URL", "http://localhost:8000")
        init = Initialize(token="token")
        init.bikes = None

        mock_bike_data = {
            "data": [
                {
                    "id": 101,
                    "attributes": {"last_position": "POINT(13.06782 55.577859)"}
                },
                {
                    "id": 102,
                    "attributes": {"last_position": "POINT(13.46782 54.977859)"}
                }
            ]
        }

        with patch("httpx.AsyncClient", autospec=True) as mock_client_class:
            mock_client_instance = MagicMock()
            mock_client_class.return_value.__aenter__.return_value = mock_client_instance
            mock_client_instance.get = AsyncMock(
                return_value=_mock_response(json_data=mock_bike_data))
            positions_str = await init.bike_positions()
            assert positions_str == "13.06782:55.577859,13.46782:54.977859"

class TestExtract:
    """Tests for the Extract class."""
    def test_extract_bike_ids(self):
        """Test that Extract.Bike.ids() extracts bike IDs."""
        bikes = [
            {"id": 10, "attributes": {"last_position": "POINT(1 2)"}},
            {"id": 20, "attributes": {"last_position": "POINT(3 4)"}}
        ]
        result = Extract.Bike.ids(bikes)
        assert result == [10, 20]

    def test_extract_bike_positions(self):
        """Test that Extract.Bike.positions() extracts bike positions."""
        bikes = [
            {"id": 10, "attributes": {"last_position": "POINT(13.0 55.0)"}},
            {"id": 20, "attributes": {"last_position": "POINT(14.5 56.25)"}}
        ]
        result = Extract.Bike.positions(bikes)
        assert result == [(13.0, 55.0), (14.5, 56.25)]

class TestSerialize:
    """Tests for the Serialize class."""
    def test_serialize_bike_ids(self):
        """Test that Serialize.bike_ids() serializes a list of bike IDs."""
        ids = [10, 20, 30]
        result = Serialize.bike_ids(ids)
        assert result == "10,20,30"

    def test_serialize_positions(self):
        """Test that Serialize.positions() serializes a list of positions."""
        positions = [(13.06782, 55.577859), (13.46782, 54.977859)]
        result = Serialize.positions(positions)
        assert result == "13.06782:55.577859,13.46782:54.977859"
