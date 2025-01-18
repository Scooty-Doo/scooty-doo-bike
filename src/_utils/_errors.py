"""
Module containing custom errors.
"""

class NotChargingZoneError(Exception):
    """Custom error raised when bike is not in a charging zone."""
    def __init__(self, message="This zone is not a charging zone."):
        super().__init__(message)

class PositionNotWithinZoneError(Exception):
    """Custom error raised when a position is not within a zone."""
    def __init__(self, message="This position is not within a zone."):
        super().__init__(message)

class AlreadyUnlockedError(Exception):
    """Custom error raised when a bike is already in use (is unlocked)."""
    def __init__(self, message="This bike is already in use (is unlocked)."):
        super().__init__(message)

class AlreadyLockedError(Exception):
    """Custom error raised when a bike is already locked."""
    def __init__(self, message="This bike is already locked."):
        super().__init__(message)

class FullyChargedError(Exception):
    """Custom error raised when a bike is already fully charged."""
    def __init__(self, message="This bike is already fully charged."):
        super().__init__(message)

class InvalidModeError(Exception):
    """Custom error raised when an invalid mode is passed."""
    def __init__(self, message="Invalid mode."):
        super().__init__(message)

class InitializationError(Exception):
    """Custom error raised when an object is not initialized properly."""
    def __init__(self, message="Object not initialized properly. "
                 "Missing required environment variables."):
        super().__init__(message)

class OutOfBoundsError(Exception):
    """Custom error raised when a bike is moved out of bounds."""
    def __init__(self, message="This position is out of bounds. "
                 "It is not in one of the zones on the map."):
        super().__init__(message)

class InvalidPositionError(Exception):
    """Custom error raised when an invalid position is passed."""
    def __init__(self, message="Invalid position. "
                 "Position must be a tuple of two floatable numbers."):
        super().__init__(message)

class InvalidPositionTypeError(Exception):
    """Custom error raised when an invalid position type is passed."""
    def __init__(self, message="Position must be a list or tuple."):
        super().__init__(message)

class InvalidPositionLengthError(Exception):
    """Custom error raised when an invalid position length is passed."""
    def __init__(self, message="Position must contain exactly two elements."):
        super().__init__(message)

class InvalidPositionCoordinatesError(Exception):
    """Custom error raised when invalid position coordinates are passed."""
    def __init__(self, message="Each coordinate in position must be an int or float."):
        super().__init__(message)

class MovingOrChargingError(Exception):
    """Custom error raised when bike is moving or charging."""
    def __init__(self, message="Bike is moving or charging and cannot accept further requests "
                 "until moving or charging is completed."):
        super().__init__(message)

class Errors():
    """Class handling the raising of custom errors."""
    @staticmethod
    def not_charging_zone():
        """Raise NotChargingZoneError."""
        raise NotChargingZoneError()

    @staticmethod
    def already_unlocked():
        """Raise AlreadyUnlockedError."""
        raise AlreadyUnlockedError()

    @staticmethod
    def already_locked():
        """Raise AlreadyLockedError."""
        raise AlreadyLockedError()

    @staticmethod
    def fully_charged():
        """Raise FullyChargedError."""
        raise FullyChargedError()

    @staticmethod
    def invalid_mode():
        """Raise InvalidModeError."""
        raise InvalidModeError()

    @staticmethod
    def initialization_error():
        """Raise InitializationError."""
        raise InitializationError()

    @staticmethod
    def out_of_bounds():
        """Raise OutOfBoundsError."""
        raise OutOfBoundsError()

    @staticmethod
    def position_not_within_zone():
        """Raise PositionNotWithinZoneError."""
        raise PositionNotWithinZoneError()

    @staticmethod
    def invalid_position():
        """Raise InvalidPositionError."""
        raise InvalidPositionError()

    @staticmethod
    def invalid_position_type():
        """Raise InvalidPositionTypeError."""
        raise InvalidPositionTypeError()

    @staticmethod
    def invalid_position_length():
        """Raise InvalidPositionLengthError."""
        raise InvalidPositionLengthError()

    @staticmethod
    def invalid_position_coordinates():
        """Raise InvalidPositionCoordinatesError."""
        raise InvalidPositionCoordinatesError()

    @staticmethod
    def moving_or_charging():
        """Raise MovingOrChargingError."""
        raise MovingOrChargingError()
