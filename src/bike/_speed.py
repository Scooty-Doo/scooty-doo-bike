from .._utils._map import Map
from .._utils._settings import Settings

class Speed:
    def __init__(self):
        self.settings = Settings.Speed()
        self.current = 0
        self.max = self.settings.max_speed

    def limit(self, zones, zone_types, position):
        """Fetch speed limit for position."""
        self.current = Map.Zone.get_speed_limit(zones, zone_types, position)
    
    def terminate(self):
        self.current = 0
    
