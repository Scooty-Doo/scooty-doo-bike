import pytest
import json
import os
from unittest.mock import patch

@pytest.fixture(scope="session")
def mock_zones():
    """Load mock zones from a local JSON file."""
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'fixtures', 'mock_zones.json')
    with open(file_path, 'r') as f:
        zones = json.load(f)
    return zones

@pytest.fixture(scope="session")
def mock_zone_types():
    """Load mock zone types from a local JSON file."""
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'fixtures', 'mock_zone_types.json')
    with open(file_path, 'r') as f:
        zone_types = json.load(f)
    return zone_types

@pytest.fixture(autouse=True)
def mock_sleep(request):
    """
    Automatically mock Clock.sleep to prevent actual sleeping during tests.
    This fixture is applied to all tests automatically due to autouse=True.
    """
    if hasattr(request.node, 'cls') and request.node.cls is not None and request.node.cls.__name__ == "TestClock":
        yield
    else:
        with patch('src._utils._clock.Clock.sleep', return_value=None):
            yield

@pytest.fixture
def mock_environment(monkeypatch):
    """Mock environment variables required for the application."""
    monkeypatch.setenv("BIKE_ID", "test_bike")
    monkeypatch.setenv("TOKEN", "test_token")
    monkeypatch.setenv("BACKEND_URL", "http://localhost:8000")
    monkeypatch.setenv("LONGITUDE", "0.0")
    monkeypatch.setenv("LATITUDE", "0.0")
    monkeypatch.setenv("PORT", "8000")

# python -m pytest
# python -m pytest -s
# python -m pytest --cov=src --cov-report=html
