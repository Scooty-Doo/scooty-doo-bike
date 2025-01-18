"""
Module containing the User class.
"""

from ._trip import Trip

class User:
    """Class representing a user."""
    def __init__(self, user_id):
        self.user_id = user_id
        self.trip = None

    def start_trip(self, bike_id, trip_id, position, zone=None):
        """Start a trip."""
        self.trip = Trip(self.user_id, bike_id, trip_id, position, zone)

    def end_trip(self, position, zone=None):
        """End a trip."""
        self.trip.end_trip(position, zone)

    def archive_trip(self):
        """Archive the trip."""
        self.trip = None
