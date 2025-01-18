"""Tests for the main module."""

from unittest.mock import patch, AsyncMock
import pytest
from src.main import main
from src._utils._clock import Clock
from src._utils._errors import InitializationError
from src.brain._initialize import Initialize

@pytest.mark.asyncio
async def test_main_success(monkeypatch):
    """Test main() success case."""
    monkeypatch.setenv("BIKE_IDS", "101,102")
    monkeypatch.setenv("TOKEN", "token")
    monkeypatch.setenv("POSITIONS", "12.34:55.55,13.45:56.66")
    with patch.object(Clock, "sleep", new=AsyncMock()) as _:
        with patch("uvicorn.Server.serve", new_callable=AsyncMock) as mock_serve:
            with patch("src.brain.brain.Brain.run", new_callable=AsyncMock) as mock_brain_run:
                with patch.object(Initialize, "_load_bikes", new=AsyncMock()) as mock_load_bikes:
                    mock_load_bikes.return_value = None
                    await main()
                    mock_serve.assert_awaited_once()
                    assert mock_brain_run.await_count == 2
                    mock_load_bikes.assert_awaited_once()

@pytest.mark.asyncio
async def test_main_fallback_init_failure(monkeypatch):
    """Test main() when _load_bikes() fails and fallback is used."""
    monkeypatch.setenv("BIKE_IDS", "201,202")
    monkeypatch.setenv("POSITIONS", "20.0:30.0,21.0:31.0")
    monkeypatch.setenv("TOKEN", "fallback-token")
    with patch.object(Clock, "sleep", new=AsyncMock()):
        with patch("uvicorn.Server.serve", new_callable=AsyncMock) as mock_serve:
            with patch("src.brain.brain.Brain.run", new_callable=AsyncMock) as mock_brain_run:
                with patch.object(Initialize, "_load_bikes", side_effect=Exception("Backend down")):
                    await main()
                    mock_serve.assert_awaited_once()
                    mock_brain_run.assert_awaited()

@pytest.mark.asyncio
async def test_main_missing_bike_ids(monkeypatch):
    """Test main() when BIKE_IDS is missing."""
    monkeypatch.delenv("BIKE_IDS", raising=False)
    monkeypatch.setenv("TOKEN", "token")
    with patch.object(Clock, "sleep", new=AsyncMock()):
        with patch("uvicorn.Server.serve", new_callable=AsyncMock) as mock_serve:
            with patch("src.brain.brain.Brain.run", new_callable=AsyncMock):
                with pytest.raises(InitializationError):
                    await main()
                mock_serve.assert_not_awaited()

@pytest.mark.asyncio
async def test_main_invalid_bike_ids(monkeypatch):
    """Test main() when BIKE_IDS is invalid."""
    monkeypatch.setenv("BIKE_IDS", "123,abc")
    monkeypatch.setenv("TOKEN", "token")
    with patch.object(Clock, "sleep", new=AsyncMock()):
        with patch("uvicorn.Server.serve", new_callable=AsyncMock) as mock_serve:
            with patch("src.brain.brain.Brain.run", new_callable=AsyncMock):
                with pytest.raises(InitializationError):
                    await main()
                mock_serve.assert_not_awaited()

@pytest.mark.asyncio
async def test_main_mismatch_bike_ids_positions(monkeypatch):
    """Test main() when BIKE_IDS and POSITIONS have different lengths."""
    monkeypatch.setenv("BIKE_IDS", "1,2,3")
    monkeypatch.setenv("POSITIONS", "13.1:55.1,14.2:56.2")
    monkeypatch.setenv("TOKEN", "token")
    with patch.object(Clock, "sleep", new=AsyncMock()):
        with patch("uvicorn.Server.serve", new_callable=AsyncMock) as mock_serve:
            with patch("src.brain.brain.Brain.run", new_callable=AsyncMock):
                with pytest.raises(InitializationError):
                    await main()
                mock_serve.assert_not_awaited()

@pytest.mark.asyncio
async def test_main_invalid_positions(monkeypatch):
    """Test main() when POSITIONS is invalid."""
    monkeypatch.setenv("BIKE_IDS", "1,2")
    monkeypatch.setenv("POSITIONS", "abc:def,12.34:56.78")
    monkeypatch.setenv("TOKEN", "token123")
    with patch.object(Clock, "sleep", new=AsyncMock()):
        with patch("uvicorn.Server.serve", new_callable=AsyncMock) as mock_serve:
            with patch("src.brain.brain.Brain.run", new_callable=AsyncMock):
                with pytest.raises(InitializationError):
                    await main()
                mock_serve.assert_not_awaited()

@pytest.mark.asyncio
async def test_main_default_positions(monkeypatch):
    """Test main() when POSITIONS is not set."""
    monkeypatch.setenv("BIKE_IDS", "10,20")
    monkeypatch.delenv("POSITIONS", raising=False)
    monkeypatch.setenv("TOKEN", "token")
    with patch.object(Clock, "sleep", new=AsyncMock()):
        with patch("uvicorn.Server.serve", new_callable=AsyncMock):
            with patch("src.brain.brain.Brain.run", new_callable=AsyncMock):
                with patch("src.brain._initialize.Initialize._load_bikes", new=AsyncMock()):
                    await main()

@pytest.mark.asyncio
async def test_main_initialize_bike_positions(monkeypatch):
    """Test main() when bikes are initialized remotely."""
    monkeypatch.setenv("BIKE_IDS", "101,102")
    monkeypatch.setenv("TOKEN", "test_token")
    monkeypatch.setenv("POSITIONS", "12.34:55.55,13.45:56.66")
    with patch.object(
        Initialize, "bike_ids",
        new=AsyncMock(return_value="101,102")
        ) as mock_bike_ids:
        with patch.object(
            Initialize, "bike_positions",
            new=AsyncMock(return_value="12.34:55.55,13.45:56.66")
            ) as mock_bike_positions:
            with patch.object(Clock, "sleep", new=AsyncMock()):
                with patch("uvicorn.Server.serve", new_callable=AsyncMock) as mock_serve:
                    with patch(
                        "src.brain.brain.Brain.run",
                        new_callable=AsyncMock
                        ) as mock_brain_run:
                        await main()
                        mock_bike_ids.assert_awaited_once()
                        mock_bike_positions.assert_awaited_once()
                        mock_serve.assert_awaited_once()
                        assert mock_brain_run.await_count == 2
