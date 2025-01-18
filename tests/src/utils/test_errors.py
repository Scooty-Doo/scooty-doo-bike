"""Tests for the Errors class."""

import pytest
from src._utils._errors import (Errors,
                                InitializationError,
                                InvalidPositionError,
                                InvalidPositionCoordinatesError,
                                MovingOrChargingError,
                                AlreadyLockedError,
                                AlreadyUnlockedError,
                                PositionNotWithinZoneError,
                                InvalidPositionTypeError)

class TestErrors:
    """Tests for the Errors class."""
    def test_initialization_error_message_default(self):
        """Test the default initialization error message."""
        with pytest.raises(InitializationError) as exc_info:
            raise InitializationError()
        assert str(exc_info.value) == \
            "Object not initialized properly. Missing required environment variables."

    def test_initialization_error_message_custom(self):
        """Test a custom initialization error message."""
        custom_message = "Custom initialization failure message."
        with pytest.raises(InitializationError) as exc_info:
            raise InitializationError(message=custom_message)
        assert str(exc_info.value) == custom_message

    def test_errors_initialization_error_raises_exception(self):
        """Test the initialization error method."""
        with pytest.raises(InitializationError) as exc_info:
            Errors.initialization_error()
        assert str(exc_info.value) == \
            "Object not initialized properly. Missing required environment variables."

    def test_invalid_position_error_message_default(self):
        """Test the default invalid position error message."""
        with pytest.raises(InvalidPositionError) as exc_info:
            raise InvalidPositionError()
        assert str(exc_info.value) == \
            "Invalid position. Position must be a tuple of two floatable numbers."

    def test_errors_invalid_position_error_raises_exception(self):
        """Test the invalid position error method."""
        with pytest.raises(InvalidPositionError) as exc_info:
            Errors.invalid_position()
        assert str(exc_info.value) == \
            "Invalid position. Position must be a tuple of two floatable numbers."

    def test_invalid_position_coordinates_error_message_default(self):
        """Test the default invalid position coordinates error message."""
        with pytest.raises(InvalidPositionCoordinatesError) as exc_info:
            raise InvalidPositionCoordinatesError()
        assert str(exc_info.value) == \
            "Each coordinate in position must be an int or float."

    def test_errors_invalid_position_coordinates_error_raises_exception(self):
        """Test the invalid position coordinates error method."""
        with pytest.raises(InvalidPositionCoordinatesError) as exc_info:
            Errors.invalid_position_coordinates()
        assert str(exc_info.value) == \
            "Each coordinate in position must be an int or float."

    def test_moving_or_charging_error_message_default(self):
        """Test the default moving or charging error message."""
        with pytest.raises(MovingOrChargingError) as exc_info:
            raise MovingOrChargingError()
        assert str(exc_info.value) == \
            "Bike is moving or charging and cannot accept further requests " \
            "until moving or charging is completed."

    def test_errors_moving_or_charging_error_raises_exception(self):
        """Test the moving or charging error method."""
        with pytest.raises(MovingOrChargingError) as exc_info:
            Errors.moving_or_charging()
        assert str(exc_info.value) == \
            "Bike is moving or charging and cannot accept further requests " \
            "until moving or charging is completed."

    def test_already_locked_error_message_default(self):
        """Test the default already locked error message."""
        with pytest.raises(AlreadyLockedError) as exc_info:
            raise AlreadyLockedError()
        assert str(exc_info.value) == "This bike is already locked."

    def test_errors_already_unlocked_error_message_default(self):
        """Test the already unlocked error method."""
        with pytest.raises(AlreadyUnlockedError) as exc_info:
            Errors.already_unlocked()
        assert str(exc_info.value) == "This bike is already in use (is unlocked)."

    def test_position_not_within_zone_error_message_default(self):
        """Test the default position not within zone error message."""
        with pytest.raises(PositionNotWithinZoneError) as exc_info:
            raise PositionNotWithinZoneError()
        assert str(exc_info.value) == "This position is not within a zone."

    def test_invalid_position_type_error_message_default(self):
        """Test the default invalid position type error message."""
        with pytest.raises(InvalidPositionTypeError) as exc_info:
            raise InvalidPositionTypeError()
        assert str(exc_info.value) == "Position must be a list or tuple."
