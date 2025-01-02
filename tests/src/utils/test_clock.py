import pytest
from src._utils._clock import Clock

class TestClock:
    @pytest.mark.asyncio
    async def test_sleep(self):
        with pytest.raises(TypeError):
            await Clock.sleep("a")
        with pytest.raises(ValueError):
            await Clock.sleep(-1)
        Clock.sleep(1)
