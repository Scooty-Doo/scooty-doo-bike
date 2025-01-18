"""Tests for the Position class."""

from src.bike._position import Position

class TestPosition:
    """Tests for the Position class."""

    def test_is_position_with_valid_coordinates(self):
        """Test is_position with valid coordinates."""
        valid_positions = [
            (0, 0),
            (1.5, 2.5),
            (-10, 20),
            (-1.2345, 0.1234)]
        for position in valid_positions:
            assert Position.is_position(position) is True, f"Failed for position: {position}"

    def test_is_position_with_invalid_coordinates(self):
        """Test is_position with invalid coordinates."""
        invalid_positions = [
            ('a', 0),
            (0, 'b'),
            (None, 1.2),
            (1.2, None),
            ([1, 2], 3),
            (3, {"x": 1}),
        ]
        for position in invalid_positions:
            assert Position.is_position(position) is False, f"Failed for position: {position}"

    def test_is_position_with_non_tuple_or_list(self):
        """Test is_position with non-tuple or non-list values."""
        non_position_types = [
            42,
            3.14,
            "not a position",
            {"x": 0, "y": 1},
            None]
        for value in non_position_types:
            assert Position.is_position(value) is False, f"Failed for value: {value}"
