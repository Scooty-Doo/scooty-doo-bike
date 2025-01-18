"""
Module for the Logs class.
"""

from .._utils._format import Format

class Logs:
    """Class handling the logs of the bike."""
    def __init__(self):
        self.logs = []

    def add(self, trip):
        """Add a log entry."""
        log = trip
        if self._exists(log):
            index = self._get_log_index(log)
            self.logs[index] = log
        else:
            self.logs.append(log)

    def update(self, trip):
        """Update a log entry."""
        self.add(trip)

    def get(self):
        """Return all logs."""
        return [Format.log(log) for log in self.logs]

    def last(self):
        """Return the last log."""
        return Format.log(self.logs[-1])

    def _exists(self, log):
        """Check if a log entry exists."""
        return any(log["trip_id"] == entry["trip_id"] for entry in self.logs)

    def _get_log_index(self, log): # @SuppressWarnings("protected-access")
        """Get the index of a log entry."""
        return [log["trip_id"] == entry["trip_id"] for entry in self.logs].index(True)
