"""Module for testing full bike functionality"""

import pytest

from fastapi.testclient import TestClient
from src.main import app
from src.brain.brain import Brain
from src.brain._incoming import get_brain
from src._utils._clock import Clock


class TestIntegration:
    """Class for testing integration"""

    @pytest.fixture
    def integration_mock_fixture(self, monkeypatch):
        """Fixture for integration testing"""
        # Create a brain instance
        brain_instance = Brain(
            bike_id=1, longitude=12.44, latitude=23.44, token="token"
        )

        # Mock get brain to always return same instance
        def mock_get_brain():
            return brain_instance

        # Monkeypatch to override get_brain
        app.dependency_overrides[get_brain] = mock_get_brain
        # Mock Clock.now so that it always returns the same value (helps with log checking)
        monkeypatch.setattr(Clock, "now", lambda: "2024-12-25T13:27:44.284455+00:00")

        return brain_instance

    correct_response_start = {
        "message": "Trip started.",
        "data": {
            "report": {
                "city_id": 1,
                "last_position": "POINT(12.44 23.44)",
                "battery_lvl": 100,
                "is_available": False,
            },
            "log": {
                "user_id": 652134919185249719,
                "bike_id": 1,
                "trip_id": 1114,
                "start_time": "2024-12-25T13:27:44.284455+00:00",
                "start_position": "POINT(12.44 23.44)",
                "path_taken": "LINESTRING(12.44 23.44, 12.44 23.44)",
                "start_map_zone_id": None,
                "start_map_zone_type": None,
            },
        },
    }

    correct_response_end = {
        "message": "Trip ended. Log and report sent",
        "data": {
            "log": {
                "user_id": 652134919185249719,
                "bike_id": 1,
                "trip_id": 1114,
                "start_time": "2024-12-25T13:27:44.284455+00:00",
                "start_position": "POINT(12.44 23.44)",
                "end_time": "2024-12-25T13:27:44.284455+00:00",
                "end_position": "POINT(12.45 23.45)",
                "path_taken": "LINESTRING(12.44 23.44, 12.45 23.45)",
                "start_map_zone_id": None,
                "start_map_zone_type": None,
                "end_map_zone_id": None,
                "end_map_zone_type": None,
            },
            "report": {
                "city_id": 1,
                "last_position": "POINT(12.45 23.45)",
                "battery_lvl": 100,
                "is_available": True,
            },
        },
    }

    correct_response_end_no_move = {
        "message": "Trip ended. Log and report sent",
        "data": {
            "log": {
                "user_id": 652134919185249719,
                "bike_id": 1,
                "trip_id": 1114,
                "start_time": "2024-12-25T13:27:44.284455+00:00",
                "start_position": "POINT(12.44 23.44)",
                "end_time": "2024-12-25T13:27:44.284455+00:00",
                "end_position": "POINT(12.44 23.44)",
                "path_taken": "LINESTRING(12.44 23.44, 12.44 23.44)",
                "start_map_zone_id": None,
                "start_map_zone_type": None,
                "end_map_zone_id": None,
                "end_map_zone_type": None,
            },
            "report": {
                "city_id": 1,
                "last_position": "POINT(12.44 23.44)",
                "battery_lvl": 100,
                "is_available": True,
            },
        },
    }

    def test_api_startup(self):
        """Tests if api starts"""
        # Setup
        client = TestClient(app)
        # Act
        response = client.get("/docs")
        # Assert
        assert response.status_code == 200

    @pytest.mark.usefixtures("integration_mock_fixture")
    def test_start_trip(self):
        """Tests if start trip route works"""
        # Setup
        client = TestClient(app)

        # Act
        response = client.post(
            "/start_trip", json={"user_id": 652134919185249719, "trip_id": 1114}
        )

        # Assert
        assert response.status_code == 200
        assert "Trip started." in response.json()["message"]
        assert response.json() == self.correct_response_start

    @pytest.mark.usefixtures("integration_mock_fixture")
    def test_whole_trip(self, monkeypatch):
        """Tests if end_trip route works"""
        # Setup
        client = TestClient(app)
        monkeypatch.setenv("DEFAULT_SPEED", "2000.0")

        # Act
        # Start trip:
        start_response = client.post(
            "/start_trip", json={"user_id": 652134919185249719, "trip_id": 1114}
        )

        if start_response.status_code != 200:
            print(start_response.json())
        assert start_response.status_code == 200

        # Move bike once:
        move_response = client.post(
            "move", json={"position_or_linestring": [[12.45, 23.45]]}
        )

        assert move_response.status_code == 200

        # End trip:
        end_response = client.post(
            "end_trip", json={"maintenance": False, "ignore_zone": True}
        )

        assert end_response.status_code == 200
        assert end_response.json() == self.correct_response_end

    @pytest.mark.usefixtures("integration_mock_fixture")
    def test_whole_trip_no_move(self):
        """Tests if end_trip route works"""
        # Setup
        client = TestClient(app)

        # Act
        # Start trip:
        start_response = client.post(
            "/start_trip", json={"user_id": 652134919185249719, "trip_id": 1114}
        )

        assert start_response.status_code == 200

        # End trip:
        end_response = client.post(
            "end_trip", json={"maintenance": False, "ignore_zone": True}
        )
        if end_response.status_code != 200:
            print(end_response.json())
        assert end_response.status_code == 200
        assert end_response.json() == self.correct_response_end_no_move
