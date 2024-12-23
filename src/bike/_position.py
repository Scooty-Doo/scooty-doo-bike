from .._utils._validate import Validate

class Position:
    def __init__(self, longitude, latitude):
        self.longitude = float(longitude)
        self.latitude = float(latitude)
        self.current = (self.longitude, self.latitude)

    def change(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude
        self.current = (longitude, latitude)

    def is_valid(self, position):
        return Validate.is_valid_position(position)