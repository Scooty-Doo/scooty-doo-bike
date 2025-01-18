"""
Module for the Status class.
"""

import copy
from .._utils._clock import Clock

class Status:
    """Class representing the status of a bike."""
    def __init__(self, bike):
        self.update(bike)

    def update(self, bike):
        """Update the status of the bike."""
        self.bike_id = bike.bike_id
        self.mode = bike.mode.current
        self.battery_level = bike.battery.level
        self.speed = bike.speed.current
        self.position = bike.position.current
        self.timestamp = Clock.now()
        self.city_id = bike.city.id

    def get(self, bike):
        """Return the status of the bike."""
        self.update(bike)
        return copy.deepcopy(self.__dict__)
