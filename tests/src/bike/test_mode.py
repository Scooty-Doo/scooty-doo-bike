"""Tests for the Mode class."""

import pytest
from src.bike._mode import Mode
from src._utils._errors import InvalidModeError

class TestMode:
    """Tests for the Mode class."""

    def test_initial_mode(self):
        """Test the initial mode."""
        mode = Mode()
        assert mode.current == 'sleep'

    def test_initial_mode_custom(self):
        """Test the initial mode with a custom mode."""
        mode = Mode(mode='maintenance')
        assert mode.current == 'maintenance'

    def test_invalid_initial_mode(self):
        """Test an invalid initial mode."""
        with pytest.raises(InvalidModeError):
            Mode(mode='invalid')

    def test_usage_mode_transition(self):
        """Test transitioning to the usage mode."""
        mode = Mode()
        mode.usage()
        assert mode.current == 'usage'
        assert mode.is_unlocked()
        assert not mode.is_locked()

    def test_maintenance_mode_transition(self):
        """Test transitioning to the maintenance mode."""
        mode = Mode()
        mode.maintenance()
        assert mode.current == 'maintenance'
        assert not mode.is_unlocked()
        assert mode.is_locked()

    def test_sleep_mode_transition(self):
        """Test transitioning to the sleep mode."""
        mode = Mode()
        mode.sleep()
        assert mode.current == 'sleep'
        assert not mode.is_unlocked()
        assert mode.is_locked()

    def test_is_usage(self):
        """Test the is_usage method."""
        mode = Mode()
        mode.usage()
        assert mode.is_usage() is True
        mode.sleep()
        assert mode.is_usage() is False

    def test_is_maintenance(self):
        """Test the is_maintenance method."""
        mode = Mode()
        mode.maintenance()
        assert mode.is_maintenance() is True
        mode.usage()
        assert mode.is_maintenance() is False

    def test_is_sleep(self):
        """Test the is_sleep method."""
        mode = Mode()
        mode.sleep()
        assert mode.is_sleep() is True
        mode.usage()
        assert mode.is_sleep() is False

    def test_is_unlocked(self):
        """Test the is_unlocked method."""
        mode = Mode()
        mode.usage()
        assert mode.is_unlocked() is True
        mode.sleep()
        assert mode.is_unlocked() is False

    def test_is_locked(self):
        """Test the is_locked method."""
        mode = Mode()
        assert mode.is_locked() is True
        mode.usage()
        assert mode.is_locked() is False
        mode.sleep()
        assert mode.is_locked() is True

    def test_invalid_mode_raises_exception(self):
        """Test that an invalid mode raises an InvalidModeError."""
        invalid_mode = 'flying'
        with pytest.raises(InvalidModeError) as exc_info:
            Mode(mode=invalid_mode)

        assert str(exc_info.value) == "Invalid mode."

    def test_initial_submodes(self):
        """Test the initial submodes."""
        mode = Mode()
        assert mode.submodes.usage.moving is False
        assert mode.submodes.usage.charging is False

    def test_is_moving(self):
        """Test the is_moving method."""
        mode = Mode()
        mode.submodes.usage.moving = True
        assert mode.submodes.usage.is_moving()
        mode.submodes.usage.moving = False
        assert not mode.submodes.usage.is_moving()

    def test_is_charging(self):
        """Test the is_charging method."""
        mode = Mode()
        mode.submodes.usage.charging = True
        assert mode.submodes.usage.is_charging()
        mode.submodes.usage.charging = False
        assert not mode.submodes.usage.is_charging()
