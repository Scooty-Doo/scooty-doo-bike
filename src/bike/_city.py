"""
Module for the City class.
"""

from .._utils._map import Map

class City:
    """Class representing the city the bike is in."""
    def __init__(self):
        self.id = None
        self.zones = None

    def switch(self, zones, position):
        """Switch the city based on the position."""
        closest_zone = Map.Position.get_closest_zone(zones, position)
        self.id = Map.Zone.get_city_id(closest_zone)
        self.zones = Map.Zones.get_zones_with_city_id(zones, self.id)
