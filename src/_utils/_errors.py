# TODO: remove if not used
#class NotParkingZoneError(Exception):
#    """Custom error raised when bike is in a non-parking zone."""
#    def __init__(self, message="This zone is not a parking zone."):
#        super().__init__(message)

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
    def __init__(self, message="Object not initialized properly. Missing required environment variables."):
        super().__init__(message)

class OutOfBoundsError(Exception):
    """Custom error raised when a bike is moved out of bounds."""
    def __init__(self, message="This position is out of bounds. It is not in one of the zones on the map."):
        super().__init__(message)

class Errors():
    # TODO: remove if not used
    #@staticmethod
    #def not_parking_zone(): 
    #    raise NotParkingZoneError()
    
    def not_charging_zone():
        raise NotChargingZoneError()

    @staticmethod
    def already_unlocked():
        raise AlreadyUnlockedError()
    
    @staticmethod
    def already_locked():
        raise AlreadyLockedError()
    
    @staticmethod
    def fully_charged():
        raise FullyChargedError()

    @staticmethod
    def invalid_mode():
        raise InvalidModeError()

    @staticmethod
    def initialization_error():
        raise InitializationError()
    
    @staticmethod
    def out_of_bounds():
        raise OutOfBoundsError()
    
    @staticmethod
    def position_not_within_zone():
        raise PositionNotWithinZoneError()