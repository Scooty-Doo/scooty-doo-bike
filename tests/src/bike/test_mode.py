import pytest
from src.bike._mode import Mode
from src._utils._errors import InvalidModeError

class TestMode:

    def test_initial_mode(self):
        mode = Mode()
        assert mode.current == 'sleep'

    def test_initial_mode_custom(self):
        mode = Mode(mode='maintenance')
        assert mode.current == 'maintenance'

    def test_invalid_initial_mode(self):
        with pytest.raises(InvalidModeError):
            Mode(mode='invalid')

    def test_usage_mode_transition(self):
        mode = Mode()
        mode.usage()
        assert mode.current == 'usage'
        assert mode.is_unlocked()
        assert not mode.is_locked()

    def test_maintenance_mode_transition(self):
        mode = Mode()
        mode.maintenance()
        assert mode.current == 'maintenance'
        assert not mode.is_unlocked()
        assert mode.is_locked()

    def test_sleep_mode_transition(self):
        mode = Mode()
        mode.sleep()
        assert mode.current == 'sleep'
        assert not mode.is_unlocked()
        assert mode.is_locked()

    def test_is_usage(self):
        mode = Mode()
        mode.usage()
        assert mode.is_usage() is True
        mode.sleep()
        assert mode.is_usage() is False

    def test_is_maintenance(self):
        mode = Mode()
        mode.maintenance()
        assert mode.is_maintenance() is True
        mode.usage()
        assert mode.is_maintenance() is False

    def test_is_sleep(self):
        mode = Mode()
        mode.sleep()
        assert mode.is_sleep() is True
        mode.usage()
        assert mode.is_sleep() is False

    def test_is_unlocked(self):
        mode = Mode()
        mode.usage()
        assert mode.is_unlocked() is True
        mode.sleep()
        assert mode.is_unlocked() is False

    def test_is_locked(self):
        mode = Mode()
        assert mode.is_locked() is True
        mode.usage()
        assert mode.is_locked() is False
        mode.sleep()
        assert mode.is_locked() is True

    def test_invalid_mode_raises_exception(self):
        invalid_mode = 'flying'
        with pytest.raises(InvalidModeError) as exc_info:
            Mode(mode=invalid_mode)

        assert str(exc_info.value) == "Invalid mode."
