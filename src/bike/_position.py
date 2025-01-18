"""
Module for the Position class.
"""

class Position:
    """Class representing the position of the bike."""
    def __init__(self, longitude, latitude):
        self.longitude = float(longitude)
        self.latitude = float(latitude)
        self.current = (self.longitude, self.latitude)

    def change(self, longitude, latitude):
        """Change the position."""
        self.longitude = longitude
        self.latitude = latitude
        self.current = (longitude, latitude)

    @staticmethod
    def is_position(position):
        """Check if the position is valid."""
        if not isinstance(position, (list, tuple)):
            return False
        if len(position) != 2:
            return False
        if not all(isinstance(coordinates, (int, float)) for coordinates in position):
            return False
        return True
