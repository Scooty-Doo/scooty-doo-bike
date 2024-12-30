from ..bike._position import Position
from .._utils._errors import (Errors,
                              InvalidPositionTypeError,
                              InvalidPositionLengthError,
                              InvalidPositionCoordinatesError)

class Validate:

    @staticmethod
    def position(position):
        if not isinstance(position, (list, tuple)):
            raise Errors.invalid_position_type()
        if len(position) != 2:
            raise Errors.invalid_position_length()
        if not all(isinstance(coordinate, (int, float)) for coordinate in position):
            raise Errors.invalid_position_coordinates()
        return True

    @staticmethod
    def position_or_linestring(position_or_linestring):
        def _position_or_linestring(position_or_linestring):
            if Position.is_position(position_or_linestring):
                return True
            if not isinstance(position_or_linestring, (list, tuple)):
                raise Errors.invalid_position_type()
            for position in position_or_linestring:
                if not isinstance(position, (list, tuple)):
                    raise Errors.invalid_position_length()
                Validate.position(position)
            return True
        try:
            return _position_or_linestring(position_or_linestring)
        except InvalidPositionTypeError as exc:
            raise Errors.invalid_position_type() from exc
        except InvalidPositionLengthError as exc:
            raise Errors.invalid_position_length() from exc
        except InvalidPositionCoordinatesError as exc:
            raise Errors.invalid_position_coordinates() from exc

    @staticmethod
    def is_linestring(linestring):
        if not isinstance(linestring, (list, tuple)):
            return False
        for position in linestring:
            if not Position.is_position(position):
                return False
        return True
