
from .._utils._clock import Clock

class Trip:
    def __init__(self, user_id, bike_id, trip_id, position):
        self.user_id = user_id
        self.bike_id = bike_id
        self.id = trip_id
        self.start_time = Clock.now()
        self.start_position = position

    def end_trip(self, position, route=None, distance=None, duration=None):
        self.end_time = Clock.now()
        self.end_position = position
        self.distance = distance # TODO: keep?
        self.duration = duration # TODO: keep?
        self.route = route # TODO: keep?
    
    def add_route(self, linestring):
        self.route = linestring