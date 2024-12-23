from _utils._format import Format

class TestFormatter:

    def test_format_log_entry(self):
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
        report_entry = {
            "id": 1,
            "mode": "sleeping",
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
            "is_available": True
        }
        assert formatted == expected

    def test_format_remove_fields(self):
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
        entry = {
            "trip_id": 456,
            "route": [(0.0, 0.0)]
        }
        formatted = Format._apply_all_formatting(entry)
        expected = {
            "trip_id": 456,
            "path_taken": None
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