import pytest
from src._utils._errors import Errors, InitializationError

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
