"""Tests for the Settings class."""

from src._utils._settings import Settings

class TestBikesEndpoints:
    """Tests for the bikes endpoints."""

    def test_get_all(self):
        """Test getting all bikes."""
        expected = 'v1/bikes/'
        assert Settings.Endpoints.Bikes.get_all() == expected

    def test_get(self):
        """Test getting a bike."""
        bike_id = 123
        expected = f'v1/bikes/{bike_id}'
        assert Settings.Endpoints.Bikes.get(bike_id) == expected

    def test_add(self):
        """Test adding a bike."""
        expected = 'v1/bikes/'
        assert Settings.Endpoints.Bikes.add() == expected

    def test_update(self):
        """Test updating a bike."""
        bike_id = 456
        expected = f'v1/bikes/{bike_id}'
        assert Settings.Endpoints.Bikes.update(bike_id) == expected

    def test_remove(self):
        """Test removing a bike."""
        bike_id = 789
        expected = f'v1/bikes/{bike_id}'
        assert Settings.Endpoints.Bikes.remove(bike_id) == expected
