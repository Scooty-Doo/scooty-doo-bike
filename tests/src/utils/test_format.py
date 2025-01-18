"""Tests for the Format class."""

from src._utils._format import Format

class TestFormatter:
    """Tests for the Format class."""

    def test_format_log_entry(self):
        """Test formatting a log entry."""
        log_entry = {
            "trip_id": 456,
            "user_id": 123,
            "bike_id": 1,
            "route": [(0.0, 0.0), (0.001, 0.001)],
            "start_position": (0.0, 0.0),
            "end_position": (0.001, 0.001)
        }
        formatted = Format._apply_all_formatting(log_entry)

        expected = {
            "trip_id": 456,
            "user_id": 123,
            "bike_id": 1,
            "path_taken": "LINESTRING(0 0, 0.001 0.001)",
            "start_position": "POINT(0 0)",
            "end_position": "POINT(0.001 0.001)"
        }
        assert formatted == expected

    def test_format_report_entry(self):
        """Test formatting a report entry."""
        report_entry = {
            "id": 1,
            "mode": "sleep",
            "battery_level": 75.5,
            "speed": 10,
            "position": (0.002, 0.002),
            "timestamp": "2024-12-23T12:00:00+00:00",
            "distance": 5
        }
        formatted = Format._apply_all_formatting(report_entry)

        expected = {
            "last_position": "POINT(0.002 0.002)",
            "battery_lvl": 76,  # Ceil of 75.5
            "speed": 10,
            "is_available": True
        }
        assert formatted == expected

    def test_format_remove_fields(self):
        """Test removing fields from an entry."""
        entry = {
            "trip_id": 456,
            "route": [(0.0, 0.0), (0.001, 0.001)],
            "duration": 30,
            "distance": 10
        }
        formatted = Format._apply_all_formatting(entry)
        expected = {
            "trip_id": 456,
            "path_taken": "LINESTRING(0 0, 0.001 0.001)"
        }
        assert formatted == expected

    def test_format_encode_none_path_taken(self):
        """Test that a none path_taken is formatted correctly."""
        entry = {
            "trip_id": 456,
            "route": [(0.0, 0.0)]
        }
        formatted = Format._apply_all_formatting(entry)
        expected = {
            "trip_id": 456,
            "path_taken": "LINESTRING(0 0, 0 0)"
        }
        assert formatted == expected

    def test_format_log_entry_with_id(self):
        """
        Test that the 'id' key is correctly renamed to 'trip_id' in log entries.
        """
        log_entry = {
            "id": 456,
            "user_id": 123,
            "bike_id": 1,
            "route": [(0.0, 0.0), (0.001, 0.001)],
            "start_position": (0.0, 0.0),
            "end_position": (0.001, 0.001)
        }
        formatted = Format._apply_all_formatting(log_entry)
        expected = {
            "trip_id": 456,
            "user_id": 123,
            "bike_id": 1,
            "path_taken": "LINESTRING(0 0, 0.001 0.001)",
            "start_position": "POINT(0 0)",
            "end_position": "POINT(0.001 0.001)"
        }
        assert formatted == expected

    def test_format_empty_route_with_start_position(self):
        """Test that an empty route with a start position is formatted correctly."""
        entry = {
            "trip_id": 456,
            "route": None,  # Route is None
            "start_position": (0.0, 0.0)  # Start position is provided
        }
        formatted = Format._apply_all_formatting(entry)
        expected = {
            "trip_id": 456,
            "start_position": "POINT(0 0)",
            "path_taken": "LINESTRING(0 0, 0 0)"  # LineString from start_position repeated
        }
        assert formatted == expected
