from ._trip import Trip

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.trip = None

    def start_trip(self, bike_id, trip_id, position):
        self.trip = Trip(self.user_id, bike_id, trip_id, position)
        
    def end_trip(self, position):
        self.trip.end_trip(position)
    
    def archive_trip(self): 
        self.trip = None