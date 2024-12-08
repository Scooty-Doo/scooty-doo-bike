
from .._utils._clock import Clock
import uuid

class Trip:
    def __init__(self, user_id, bike_id, position):
        self.user_id = user_id
        self.bike_id = bike_id
        self.trip_id = uuid()
        self.start_time = Clock.now()
        self.start_longitude = position[0]
        self.start_latitude = position[1]

    def end_trip(self, position, route=None, distance=None, duration=None):
        self.end_time = Clock.now()
        self.end_longitude = position[0]
        self.end_latitude = position[1]
        self.distance = distance # TODO: keep?
        self.duration = duration # TODO: keep?
        self.route = route # TODO: keep?