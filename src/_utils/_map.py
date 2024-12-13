from shapely.geometry import Point, Polygon, LineString
from shapely.wkt import loads as wkt_loads
import random

import json
import os

ZONES_FILENAME = '_zones.json'
ZONE_TYPES_FILENAME = '_zone_types.json'

# _zones.json
# [
#     {
#         "id": 1,
#         "zone_name": "zone1",
#         "zone_type": "parking",
#         "city": "city1",
#         "boundary": "Polygon(...)"
#     },
# ]

class Map:
    class Zone:
        @staticmethod
        def get(zones, position):
            point = Point(position)
            for zone in zones:
                boundary = wkt_loads(zone['boundary'])
                if point.within(boundary):
                    return zone 
        
        @staticmethod
        def get_position(zone):
            """Returns the centroid of the zone."""
            boundary = wkt_loads(zone['boundary'])
            return (boundary.centroid.x, boundary.centroid.y)
        
        @staticmethod
        def get_speed_limit(zones, zone_types, position):
            zone = Map.Zone.get(zones, position)
            zone_type = zone['zone_type']
            speed_limit = zone_types[zone_type]['speed_limit']
            return speed_limit

        @staticmethod
        def is_parking_zone(zones, position):
            zone = Map.Zone.get(zones, position)
            if zone['zone_type'] == 'parking':
                return True

        @staticmethod
        def is_charging_zone(parking_zones, position):
            zone = Map.Zone.get(parking_zones, position)
            if zone['zone_type'] == 'charging':
                return True
            
        @staticmethod
        def get_deployment_zone(zones):
            parking_zones = Map.Zones.get_parking_zones(zones)
            random_parking_zone = random.choice(parking_zones)
            return random_parking_zone

    class Zones:
        @staticmethod
        def load():
            current_directory = os.path.dirname(__file__)
            file_path = os.path.join(current_directory, ZONES_FILENAME)
            with open(file_path) as f:
                zones = json.load(f)
                if not zones:
                    return []
            return zones

        @staticmethod
        def get_parking_zones(zones):
            return [zone for zone in zones if zone['zone_type'] == 'parking']
        
        @staticmethod
        def get_charging_zones(zones):
            return [zone for zone in zones if zone['zone_type'] == 'charging']
        
        @staticmethod
        def get_slow_zones(zones):
            return [zone for zone in zones if zone['zone_type'] == 'slow']

    class ZoneTypes:
        @staticmethod
        def load():
            current_directory = os.path.dirname(__file__)
            file_path = os.path.join(current_directory, ZONE_TYPES_FILENAME)
            with open(file_path) as f:
                zone_types = json.load(f)
                if not zone_types:
                    return []
            return zone_types