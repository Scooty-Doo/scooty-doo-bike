import pytest
from src._utils._errors import Errors, InitializationError, InvalidPositionError, InvalidPositionCoordinatesError

class TestErrors:
    def test_initialization_error_message_default(self):
        with pytest.raises(InitializationError) as exc_info:
            raise InitializationError()
        assert str(exc_info.value) == "Object not initialized properly. Missing required environment variables."

    def test_initialization_error_message_custom(self):
        custom_message = "Custom initialization failure message."
        with pytest.raises(InitializationError) as exc_info:
            raise InitializationError(message=custom_message)
        assert str(exc_info.value) == custom_message

    def test_errors_initialization_error_raises_exception(self):
        with pytest.raises(InitializationError) as exc_info:
            Errors.initialization_error()
        assert str(exc_info.value) == "Object not initialized properly. Missing required environment variables."

    def test_invalid_position_error_message_default(self):
        with pytest.raises(InvalidPositionError) as exc_info:
            raise InvalidPositionError()
        assert str(exc_info.value) == "Invalid position. Position must be a tuple of two floatable numbers."

    def test_errors_invalid_position_error_raises_exception(self):
        with pytest.raises(InvalidPositionError) as exc_info:
            Errors.invalid_position()
        assert str(exc_info.value) == "Invalid position. Position must be a tuple of two floatable numbers."

    def test_invalid_position_coordinates_error_message_default(self):
        with pytest.raises(InvalidPositionCoordinatesError) as exc_info:
            raise InvalidPositionCoordinatesError()
        assert str(exc_info.value) == "Each coordinate in position must be an int or float."
    
    def test_errors_invalid_position_coordinates_error_raises_exception(self):
        with pytest.raises(InvalidPositionCoordinatesError) as exc_info:
            Errors.invalid_position_coordinates()
        assert str(exc_info.value) == "Each coordinate in position must be an int or float."