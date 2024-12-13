from .._utils._map import Map
from .._utils._settings import Settings

class Speed:
    def __init__(self):
        self.settings = Settings.Speed()
        self.current = 0
        self.max = self.settings.max_speed

    def limit(self, zones, position):
        """Set current speed to speed limit."""
        return Map.Zone.get_speed_limit(zones, position)
    
    def terminate(self):
        self.current = 0
    
