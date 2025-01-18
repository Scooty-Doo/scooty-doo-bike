import json
import os
import pytest
import pytest_asyncio

@pytest.fixture(scope="function", autouse=True)
def set_default_speed(monkeypatch):
    """Fixture to set DEFAULT_SPEED to 2000 for tests."""
    monkeypatch.setenv("DEFAULT_SPEED", "2000.0")

@pytest_asyncio.fixture(scope="session")
def mock_zones():
    """Load mock zones from a local JSON file."""
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'fixtures', 'mock_zones.json')
    with open(file=file_path, mode='r', encoding='utf-8') as f:
        zones = json.load(f)
    return zones

@pytest_asyncio.fixture(scope="session")
def mock_zone_types():
    """Load mock zone types from a local JSON file."""
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'fixtures', 'mock_zone_types.json')
    with open(file=file_path, mode='r', encoding='utf-8') as f:
        zone_types = json.load(f)
    return zone_types

@pytest_asyncio.fixture
def sample_zones_for_test_map():
    return [
        {
            "id": 1,
            "zone_type": "parking",
            "city_id": "city1",
            "boundary": "POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))"
        },
        {
            "id": 2,
            "zone_type": "charging",
            "city_id": "city1",
            "boundary": "POLYGON((2 0, 2 1, 3 1, 3 0, 2 0))"
        },
        {
            "id": 3,
            "zone_type": "slow",
            "city_id": "city1",
            "boundary": "POLYGON((4 0, 4 1, 5 1, 5 0, 4 0))"
        },
        {
            "id": 4,
            "zone_type": "parking",
            "city_id": "city1",
            "boundary": "POLYGON((6 0, 6 1, 7 1, 7 0, 6 0))"
        }
    ]

@pytest_asyncio.fixture
def sample_zone_types_for_test_map():
    return {
        "parking": {
            "speed_limit": 5
        },
        "charging": {
            "speed_limit": 5
        },
        "slow": {
            "speed_limit": 10
        },
        "regular": {
            "speed_limit": 20
        }
    }

@pytest_asyncio.fixture
def mock_environment(monkeypatch):
    """Mock environment variables required for the application."""
    monkeypatch.setenv("BIKE_ID", "test_bike")
    monkeypatch.setenv("TOKEN", "test_token")
    monkeypatch.setenv("BACKEND_URL", "http://localhost:8000/")
    monkeypatch.setenv("LONGITUDE", "0.0")
    monkeypatch.setenv("LATITUDE", "0.0")
    monkeypatch.setenv("PORT", "8000")

# python -m pytest
# python -m pytest -s
# python -m pytest --cov=src --cov-report=html
# python -m pytest --cov=src --cov-report=html --cov-report=term-missing
# python -m pytest -W error --cov=src --cov-report=html
# python -m pytest --cov=src --cov-report=html --verbose -vv
