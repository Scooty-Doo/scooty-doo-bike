
from .._utils._clock import Clock
import copy

class Trip:
    def __init__(self, user_id, bike_id, trip_id, position):
        self.user_id = user_id
        self.bike_id = bike_id
        self.trip_id = trip_id
        self.start_time = Clock.now()
        self.start_position = position
        self.route = [self.start_position]

    def end_trip(self, position):
        self.end_time = Clock.now()
        self.end_position = position
    
    def add_movement(self, position):
        self.route.append(position)

    def get(self):
        return copy.deepcopy(self.__dict__)