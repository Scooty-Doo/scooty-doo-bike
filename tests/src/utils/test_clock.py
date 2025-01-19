# pylint: disable=too-few-public-methods
"""Tests for Clock class."""

from unittest.mock import patch, AsyncMock
import pytest
from src._utils._clock import Clock

class TestClock:
    """Tests for the Clock class."""
    @pytest.mark.asyncio
    async def test_sleep(self):
        """Test the sleep method."""
        with patch('asyncio.sleep', new=AsyncMock()):
            with pytest.raises(TypeError):
                await Clock.sleep("a")
            with pytest.raises(ValueError):
                await Clock.sleep(-1)
            await Clock.sleep(1)
