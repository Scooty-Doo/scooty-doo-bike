import pytest
from src._utils._clock import Clock

class TestClock:

    def test_sleep(self):
        with pytest.raises(TypeError):
            Clock.sleep("a")
        with pytest.raises(ValueError):
            Clock.sleep(-1)
        Clock.sleep(1)