from ._trip import Trip

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.trip = None

    def start_trip(self, bike_id, trip_id, position, zone=None):
        self.trip = Trip(self.user_id, bike_id, trip_id, position, zone)

    def end_trip(self, position, zone=None):
        self.trip.end_trip(position, zone)

    def archive_trip(self):
        self.trip = None
