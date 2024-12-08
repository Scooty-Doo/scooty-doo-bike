from ._trip import Trip
import uuid

class User:
    def __init__(self, user_id=None):
        self.user_id = uuid() if user_id is None else user_id
        self.trip = None

    def start_trip(self, bike_id, position):
        self.trip = Trip(self.user_id, bike_id, position)
        
    def end_trip(self, position):
        self.trip.end_trip(position)
        self.trip = None