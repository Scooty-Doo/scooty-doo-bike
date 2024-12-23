import pytest
from src._utils._validate import Validate
from src._utils._errors import (
    InvalidPositionTypeError,
    InvalidPositionLengthError,
    InvalidPositionCoordinatesError
)

class TestValidate:

    def test_position_valid(self):
        valid_positions = [
            (0, 0),
            (1.5, -2.5),
            [-10, 20],
            [-1.2345, 0.1234]
        ]
        for position in valid_positions:
            assert Validate.position(position) is True

    def test_position_invalid_type(self):
        invalid_positions = [
            "not a position",
            None,
            123,
            {"x": 1, "y": 2}
        ]
        for position in invalid_positions:
            with pytest.raises(InvalidPositionTypeError):
                Validate.position(position)

    def test_position_invalid_length(self):
        invalid_positions = [
            (1,),
            [],
            (1, 2, 3),
            [1, 2, 3],
        ]
        for position in invalid_positions:
            with pytest.raises(InvalidPositionLengthError):
                Validate.position(position)

    def test_position_invalid_coordinates(self):
        invalid_positions = [
            ("a", 1),
            (1, "b"),
            ([1, 2], 3),
            (None, 2),
        ]
        for position in invalid_positions:
            with pytest.raises(InvalidPositionCoordinatesError):
                Validate.position(position)

    def test_position_or_linestring_valid(self):
        valid_inputs = [
            (0, 0),
            [0, 0],
            [(1, 1), (2, 2)],
            [[1.1, 1.2], [2.1, 2.2]],
        ]
        for position_or_linestring in valid_inputs:
            assert Validate.position_or_linestring(position_or_linestring) is True

    def test_position_or_linestring_invalid_type(self):
        invalid_inputs = [
            "invalid_type",
            123,
            None,
            {"x": 1, "y": 2}
        ]
        for position_or_linestring in invalid_inputs:
            with pytest.raises(InvalidPositionTypeError):
                Validate.position_or_linestring(position_or_linestring)

    def test_position_or_linestring_invalid_length(self):
        invalid_inputs = [
            [(1,)],
            [(1, 2, 3)],
            [[], []],
        ]
        for position_or_linestring in invalid_inputs:
            with pytest.raises(InvalidPositionLengthError):
                Validate.position_or_linestring(position_or_linestring)

    def test_position_or_linestring_invalid_coordinates(self):
        invalid_inputs = [
            [("a", 1)],
            [(1, "b")],
            [([1, 2], 3)],
            [(None, 2)],
        ]
        for position_or_linestring in invalid_inputs:
            with pytest.raises(InvalidPositionCoordinatesError):
                Validate.position_or_linestring(position_or_linestring)

    def test_is_linestring_valid(self):
        valid_linestrings = [
            [(0, 0), (1, 1)],
            [[1.5, -1.5], [-2.5, 2.5]],
        ]
        for linestring in valid_linestrings:
            assert Validate.is_linestring(linestring) is True

    def test_is_linestring_invalid(self):
        invalid_linestrings = [
            "not a linestring",
            123,
            None,
            {"x": 1, "y": 2},
            [(1,)],
            [(1, 2, 3)],
            [("a", 1)],
            [1, 2, 3],
        ]
        for linestring in invalid_linestrings:
            assert Validate.is_linestring(linestring) is False
