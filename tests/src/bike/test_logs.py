"""Tests for Logs class."""

import pytest
from src.bike._logs import Logs
from src._utils._format import Format

class TestLogs:
    """Tests for the Logs class."""

    def test_add_new_log(self):
        """Test adding a new log."""
        logs = Logs()
        trip = {"trip_id": 1, "user_id": 123}
        logs.add(trip)
        assert len(logs.logs) == 1
        assert logs.logs[0] == trip

    def test_add_existing_log_updates(self):
        """Test adding an existing log updates the log."""
        logs = Logs()
        trip1 = {"trip_id": 1, "user_id": 123}
        trip2 = {"trip_id": 1, "user_id": 123}
        logs.add(trip1)
        logs.add(trip2)
        assert len(logs.logs) == 1
        assert logs.logs[0] == trip2

    def test_update_log(self):
        """Test updating a log."""
        logs = Logs()
        trip1 = {"trip_id": 1, "user_id": 123}
        trip2 = {"trip_id": 1, "user_id": 123}
        logs.add(trip1)
        logs.update(trip2)
        assert len(logs.logs) == 1
        assert logs.logs[0] == trip2

    def test_get_logs(self):
        """Test getting logs."""
        logs = Logs()
        trip1 = {"trip_id": 1, "user_id": 123}
        trip2 = {"trip_id": 2, "user_id": 124}
        logs.add(trip1)
        logs.add(trip2)
        formatted_logs = logs.get()
        expected = [Format._apply_all_formatting(trip1), Format._apply_all_formatting(trip2)]
        assert formatted_logs == expected

    def test_last_log(self):
        """Test getting the last log."""
        logs = Logs()
        trip1 = {"trip_id": 1, "user_id": 123}
        trip2 = {"trip_id": 2, "user_id": 124}
        logs.add(trip1)
        logs.add(trip2)
        last_log = logs.last()
        expected = Format._apply_all_formatting(trip2)
        assert last_log == expected

    def test_get_log_index_exists(self):
        """Test getting the index of an existing log."""
        logs = Logs()
        trip = {"trip_id": 1, "user_id": 123}
        logs.add(trip)
        index = logs._get_log_index(trip)
        assert index == 0

    def test_get_log_index_not_exists(self):
        """Test getting the index of a non-existing log."""
        logs = Logs()
        trip = {"trip_id": 1, "user_id": 123}
        with pytest.raises(ValueError):
            logs._get_log_index(trip)
