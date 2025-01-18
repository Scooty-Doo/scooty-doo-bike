"""Tests for incoming routes."""

from unittest.mock import MagicMock, AsyncMock
import pytest
from fastapi.testclient import TestClient
from src.brain._incoming import app, get_brain
from src.brain.brain import Brain
from src.brain.hivemind import Hivemind
from src._utils._errors import (
    AlreadyUnlockedError,
    AlreadyLockedError,
    InvalidPositionError
)

@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)

@pytest.fixture
def mock_brain():
    """Create a mock Brain instance for testing."""
    return Brain(bike_id=1, longitude=12.34, latitude=56.78, token="fake-token")

@pytest.fixture
def override_get_brain(mock_brain):
    """Fixture to override the get_brain dependency with a mock Brain instance."""
    def _override():
        return mock_brain
    app.dependency_overrides[get_brain] = _override
    yield
    app.dependency_overrides = {}

def test_get_brain_value_error(client):
    """Test that get_brain raises HTTP 400 on ValueError."""
    app.state.hivemind = Hivemind()  # initialize empty hivemind
    response = client.post("/start_trip?bike_id=999", json={"user_id": 1, "trip_id": 1})
    assert response.status_code == 400
    assert "does not exist" in response.text

def test_no_hivemind_raises_500(client):
    """Test that get_hivemind raises HTTP 500 if hivemind is None."""
    app.state.hivemind = None
    response = client.get("/report")
    assert response.status_code == 500
    assert "Hivemind not initialized." in response.json()["detail"]

def test_root_endpoint_no_hivemind_needed(client):
    """Test the root endpoint of the API."""
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "Welcome to the bike hivemind API."}

### START TRIP ###

@pytest.mark.usefixtures("override_get_brain")
def test_start_trip_success(client, mock_brain):
    """Test starting a trip successfully."""
    mock_log = {"some": "log data"}
    mock_report = {"some": "report data"}
    mock_brain.bike.logs.last = MagicMock(return_value=mock_log)
    mock_brain.bike.reports.last = MagicMock(return_value=mock_report)
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=False)
    response = client.post("/start_trip", json={"user_id": 111, "trip_id": 222})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Trip started."
    assert data["data"]["log"] == mock_log
    assert data["data"]["report"] == mock_report

@pytest.mark.usefixtures("override_get_brain")
def test_start_trip_already_unlocked_error(client, mock_brain):
    """Test that AlreadyUnlockedError is caught and returns HTTP 400."""
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=False)
    mock_brain.bike.unlock = MagicMock(side_effect=AlreadyUnlockedError("Bike unlocked!"))
    response = client.post("/start_trip", json={"user_id": 1, "trip_id": 999})
    assert response.status_code == 400
    assert "Bike unlocked!" in response.text

@pytest.mark.usefixtures("override_get_brain")
def test_start_trip_moving_or_charging_error(client, mock_brain):
    """Test that MovingOrChargingError is caught and returns HTTP 400."""
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=True)
    response = client.post("/start_trip", json={"user_id": 123, "trip_id": 456})
    assert response.status_code == 400
    assert "Bike is moving or charging" in response.text

@pytest.mark.usefixtures("override_get_brain")
def test_start_trip_unexpected_exception(client, mock_brain):
    """Test that an unexpected exception is caught and returns HTTP 500."""
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=False)
    mock_brain.bike.unlock = MagicMock(side_effect=RuntimeError("Something went wrong!"))
    resp = client.post("/start_trip", json={"user_id": 99, "trip_id": 100})
    assert resp.status_code == 500
    assert "Internal Server Error. Details: Something went wrong!" in resp.text

### MOVE ###

@pytest.mark.usefixtures("override_get_brain")
def test_move_success(client, mock_brain):
    """Test moving the bike successfully."""
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=False)
    mock_report = {"r": "report"}
    mock_brain.bike.reports.last = MagicMock(return_value=mock_report)
    resp = client.post("/move", json={"position_or_linestring": [12.45, 23.45]})
    assert resp.status_code == 200
    data = resp.json()
    assert "Move initiated" in data["message"]
    assert data["data"]["report"] == mock_report

@pytest.mark.usefixtures("override_get_brain")
def test_move_invalid_position_error(client, mock_brain):
    """Test that InvalidPositionError is caught and returns HTTP 400."""
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=False)
    mock_brain.bike.move = MagicMock(side_effect=InvalidPositionError("Bad coordinates!"))
    resp = client.post("/move", json={"position_or_linestring": [9999, 9999]})
    assert resp.status_code == 400
    assert "Bad coordinates!" in resp.text

@pytest.mark.usefixtures("override_get_brain")
def test_move_moving_or_charging(client, mock_brain):
    """Test that MovingOrChargingError is caught and returns HTTP 400."""
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=True)
    resp = client.post("/move", json={"position_or_linestring": [12, 34]})
    assert resp.status_code == 400
    assert "Bike is moving or charging" in resp.text

@pytest.mark.usefixtures("override_get_brain")
def test_move_unexpected_exception(client, mock_brain):
    """Test that an unexpected exception is caught and returns HTTP 500."""
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=False)
    mock_brain.bike.move = MagicMock(side_effect=TypeError("Some unexpected move error"))
    resp = client.post("/move", json={"position_or_linestring": [12.45, 23.45]})
    assert resp.status_code == 500
    assert "Some unexpected move error" in resp.text
    assert "Internal Server Error. Details:" in resp.text

@pytest.mark.usefixtures("override_get_brain")
def test_move_already_locked(client, mock_brain):
    """Test that AlreadyLockedError is caught and returns HTTP 400."""
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=False)
    mock_brain.bike.move = MagicMock(side_effect=AlreadyLockedError("Bike is already locked."))
    response = client.post("/move", json={"position_or_linestring": [12.45, 23.45]})
    assert response.status_code == 400
    assert "Bike is already locked." in response.text

### RELOCATE ###

@pytest.mark.usefixtures("override_get_brain")
def test_relocate_success(client, mock_brain):
    """Test relocating the bike successfully."""
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=False)
    mock_report = {"report": "some-report"}
    mock_brain.bike.reports.last = MagicMock(return_value=mock_report)
    resp = client.post("/relocate", json={"position": [11, 22]})
    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "Relocated. Report sent."
    assert data["data"]["report"] == mock_report

@pytest.mark.usefixtures("override_get_brain")
def test_relocate_moving_or_charging(client, mock_brain):
    """Test that MovingOrChargingError is caught and returns HTTP 400."""
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=True)
    resp = client.post("/relocate", json={"position": [11, 22]})
    assert resp.status_code == 400
    assert "Bike is moving or charging" in resp.text

@pytest.mark.usefixtures("override_get_brain")
def test_relocate_already_locked_error(client, mock_brain):
    """Test that AlreadyLockedError is caught and returns HTTP 400."""
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=False)
    mock_brain.bike.relocate = MagicMock(side_effect=AlreadyLockedError("Bike is locked!"))
    response = client.post("/relocate", json={"position": [10.0, 20.0]})
    assert response.status_code == 400
    assert "Bike is locked!" in response.text

@pytest.mark.usefixtures("override_get_brain")
def test_relocate_invalid_position_error(client, mock_brain):
    """Test that InvalidPositionError is caught and returns HTTP 400."""
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=False)
    mock_brain.bike.relocate = MagicMock(side_effect=InvalidPositionError("Bad position!"))

    response = client.post("/relocate", json={"position": [9999, 9999]})
    assert response.status_code == 400
    assert "Bad position!" in response.text

@pytest.mark.usefixtures("override_get_brain")
def test_relocate_unexpected_exception(client, mock_brain):
    """Test that an unexpected exception is caught and returns HTTP 500."""
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=False)
    mock_brain.bike.relocate = MagicMock(side_effect=RuntimeError("Unexpected error."))
    response = client.post("/relocate", json={"position": [10.0, 20.0]})
    assert response.status_code == 500
    assert "Unexpected error." in response.text
    assert "Internal Server Error. Details:" in response.text

### END TRIP ###

@pytest.mark.usefixtures("override_get_brain")
def test_end_trip_success(client, mock_brain):
    """Test ending a trip successfully."""
    mock_brain.bike.lock = MagicMock()
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=False)
    mock_log = {"some": "log"}
    mock_report = {"some": "report"}
    mock_brain.bike.logs.last = MagicMock(return_value=mock_log)
    mock_brain.bike.reports.last = MagicMock(return_value=mock_report)
    resp = client.post("/end_trip", json={"maintenance": False, "ignore_zone": True})
    assert resp.status_code == 200
    data = resp.json()
    assert "Trip ended. Log and report sent" in data["message"]
    assert data["data"]["log"] == mock_log
    assert data["data"]["report"] == mock_report

@pytest.mark.usefixtures("override_get_brain")
def test_end_trip_moving_or_charging(client, mock_brain):
    """Test that MovingOrChargingError is caught and returns HTTP 400."""
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=True)
    resp = client.post("/end_trip", json={"maintenance": False, "ignore_zone": True})
    assert resp.status_code == 400
    assert "Bike is moving or charging" in resp.text

@pytest.mark.usefixtures("override_get_brain")
def test_end_trip_already_locked_error(client, mock_brain):
    """Test that AlreadyLockedError is caught and returns HTTP 400."""
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=False)
    mock_brain.bike.lock = MagicMock(side_effect=AlreadyLockedError("Already locked."))
    resp = client.post("/end_trip", json={"maintenance": False, "ignore_zone": True})
    assert resp.status_code == 400
    assert "Already locked." in resp.text

@pytest.mark.usefixtures("override_get_brain")
def test_end_trip_unexpected_exception(client, mock_brain):
    """Test that an unexpected exception is caught and returns HTTP 500."""
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=False)
    mock_brain.bike.lock = MagicMock(side_effect=RuntimeError("Something unexpected."))
    response = client.post("/end_trip", json={"maintenance": False, "ignore_zone": True})
    assert response.status_code == 500
    assert "Internal Server Error. Details: Something unexpected." in response.text

### CHECK ###

@pytest.mark.usefixtures("override_get_brain")
def test_check_success(client, mock_brain):
    """Test checking the bike successfully."""
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=False)
    mock_report = {"r": "report"}
    mock_brain.bike.reports.last = MagicMock(return_value=mock_report)
    resp = client.post("/check", json={"maintenance": True})
    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "Bike checked. Report sent"
    assert data["data"]["report"] == mock_report

@pytest.mark.usefixtures("override_get_brain")
def test_check_moving_or_charging_error(client, mock_brain):
    """Test that MovingOrChargingError is caught and returns HTTP 400."""
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=True)
    resp = client.post("/check", json={"maintenance": False})
    assert resp.status_code == 400
    assert "Bike is moving or charging" in resp.text

@pytest.mark.usefixtures("override_get_brain")
def test_check_unexpected_exception(client, mock_brain):
    """Test that an unexpected exception is caught and returns HTTP 500."""
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=False)
    mock_brain.bike.check = MagicMock(side_effect=RuntimeError("Unexpected check error!"))
    response = client.post("/check", json={"maintenance": True})
    assert response.status_code == 500
    assert "Internal Server Error. Details: Unexpected check error!" in response.text

### REPORT ###

@pytest.mark.usefixtures("override_get_brain")
def test_report_success(client, mock_brain):
    """Test creating a report successfully."""
    mock_report = {"rep": "some-report"}
    mock_brain.bike.reports.last = MagicMock(return_value=mock_report)
    resp = client.get("/report")
    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "Report created and sent"
    assert data["data"]["report"] == mock_report

@pytest.mark.usefixtures("override_get_brain")
def test_report_unexpected_exception(client, mock_brain):
    """Test that an unexpected exception is caught and returns HTTP 500."""
    mock_brain.bike.report = MagicMock(side_effect=RuntimeError("Something broke in report!"))
    response = client.get("/report")
    assert response.status_code == 500
    assert "Internal Server Error. Details: Something broke in report!" in response.text

### LOG ###

@pytest.mark.usefixtures("override_get_brain")
def test_log_success(client, mock_brain):
    """Test fetching the last log successfully."""
    mock_log = {"log": "some-log"}
    mock_brain.bike.logs.last = MagicMock(return_value=mock_log)
    resp = client.get("/log")
    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "Log created and sent"
    assert data["data"]["log"] == mock_log

@pytest.mark.usefixtures("override_get_brain")
def test_log_unexpected_exception(client, mock_brain):
    """Test that an unexpected exception is caught and returns HTTP 500."""
    mock_brain.bike.logs.last = MagicMock(side_effect=RuntimeError("Log retrieval failed!"))
    response = client.get("/log")
    assert response.status_code == 500
    assert "Internal Server Error. Details: Log retrieval failed!" in response.text

### UPDATE ###

@pytest.mark.usefixtures("override_get_brain")
def test_update_moving_or_charging(client, mock_brain):
    """Test that MovingOrChargingError is caught and returns HTTP 400."""
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=True)
    resp = client.post("/update", json={})
    assert resp.status_code == 400
    assert "Bike is moving or charging" in resp.text

@pytest.mark.usefixtures("override_get_brain")
def test_update_success(client, mock_brain):
    """Test updating the bike's zones and zone types successfully."""
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=False)
    mock_brain.request_zones = AsyncMock(return_value={"zones": "data"})
    mock_brain.request_zone_types = AsyncMock(return_value={"zone_types": "data"})
    mock_brain.bike.update = MagicMock()
    resp = client.post("/update", json={})
    assert resp.status_code == 200
    assert resp.json() == {"message": "Zones and zone types updated"}
    mock_brain.request_zones.assert_awaited_once()
    mock_brain.request_zone_types.assert_awaited_once()
    mock_brain.bike.update.assert_called_once_with(
        zones={"zones": "data"}, zone_types={"zone_types": "data"}
    )

@pytest.mark.usefixtures("override_get_brain")
def test_update_unexpected_exception(client, mock_brain):
    """Test that an unexpected exception is caught and returns HTTP 500."""
    mock_brain.bike.is_moving_or_charging = MagicMock(return_value=False)
    mock_brain.request_zones = AsyncMock(side_effect=RuntimeError("some unexpected error"))
    mock_brain.request_zone_types = AsyncMock(return_value={"zone_types": "data"})
    mock_brain.bike.update = MagicMock()
    response = client.post("/update", json={})
    assert response.status_code == 500
    resp_data = response.json()
    assert "Internal Server Error" in resp_data["detail"]
    assert "some unexpected error" in resp_data["detail"]
