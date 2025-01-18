"""
Module for the Speed class.
"""

from .._utils._map import Map
from .._utils._settings import Settings

class Speed:
    """Class handling the speed of the bike."""
    def __init__(self):
        self.settings = Settings.Speed()
        self.current = 0
        self.default = self.settings.default_speed_limit

    def limit(self, zones, zone_types, position):
        """Fetch speed limit for position."""
        speed_limit = Map.Zone.get_speed_limit(zones, zone_types, position)
        self.current = speed_limit if speed_limit else self.default

    def terminate(self):
        """Terminate the speed limit."""
        self.current = 0
