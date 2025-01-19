# pylint: disable=too-many-instance-attributes, too-many-arguments, too-many-positional-arguments, attribute-defined-outside-init
"""
This module contains the Trip class which contains information about a trip.
This is also the contents of an unformatted log.
"""

import copy
from .._utils._clock import Clock
from .._utils._map import Map

class Trip:
    """Class representing a trip."""

    def __init__(self, user_id, bike_id, trip_id, position, zone=None):
        self.user_id = user_id
        self.bike_id = bike_id
        self.trip_id = trip_id
        self.start_time = Clock.now()
        self.start_position = position
        self.route = [self.start_position]
        self.start_zone_id = None if not zone else Map.Zone.get_zone_id(zone)
        self.start_zone_type = None if not zone else Map.Zone.get_zone_type(zone)

    def end_trip(self, position, zone=None):
        """Fill in the end details of the trip."""
        self.end_time = Clock.now()
        self.end_position = position
        self.end_zone_id = None if not zone else Map.Zone.get_zone_id(zone)
        self.end_zone_type = None if not zone else Map.Zone.get_zone_type(zone)

    def add_movement(self, position):
        """Add a movement to the route."""
        self.route.append(position)

    def get(self):
        """Return a copy of the trip (i.e. an unformatted log)."""
        return copy.deepcopy(self.__dict__)
