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
#         "city_id": "city1",
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
                if boundary.covers(point):
                    return zone
            return None
        
        # TODO: remove if not used
        #@staticmethod
        #def has_city_id(zone, city_id):
        #    return Map.Zone.get_city_id(zone) == city_id
        
        @staticmethod
        def get_city_id(zone):
            return zone['city']
        
        @staticmethod
        def get_centroid_position(zone):
            """Returns the centroid of the zone."""
            boundary = wkt_loads(zone['boundary'])
            return (boundary.centroid.x, boundary.centroid.y)
        
        @staticmethod
        def get_speed_limit(zones, zone_types, position):
            zone = Map.Zone.get(zones, position)
            zone_type = zone['zone_type']
            speed_limit = zone_types[zone_type]['speed_limit']
            return speed_limit

        # TODO: remove if not used
        #@staticmethod
        #def is_parking_zone(zones, position):
        #    zone = Map.Zone.get(zones, position)
        #    if zone['zone_type'] == 'parking':
        #        return True

        @staticmethod
        def is_charging_zone(zones, position):
            zone = Map.Zone.get(zones, position)
            if zone['zone_type'] == 'charging':
                return True
        
        # TODO: remove if not used
        #@staticmethod
        #def is_forbidden_zone(zones, position):
        #    zone = Map.Zone.get(zones, position)
        #    if zone['zone_type'] == 'forbidden':
        #        return True
            
        @staticmethod
        def get_deployment_zone(zones):
            parking_zones = Map.Zones.get_parking_zones(zones)
            random_parking_zone = random.choice(parking_zones)
            return random_parking_zone
        
        @staticmethod
        def get_charging_zone(zones):
            charging_zones = Map.Zones.get_charging_zones(zones)
            random_charging_zone = random.choice(charging_zones)
            return random_charging_zone

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
        def get_zones_with_city_id(zones, city_id):
            return [zone for zone in zones if zone['city'] == city_id]

        # TODO: remove if not used
        #@staticmethod
        #def get_parking_zones(zones):
        #    return [zone for zone in zones if zone['zone_type'] == 'parking']
        
        # TODO: remove if not used
        #@staticmethod
        #def get_charging_zones(zones):
        #    return [zone for zone in zones if zone['zone_type'] == 'charging']
        
        # TODO: remove if not used
        #@staticmethod
        #def get_slow_zones(zones):
        #    return [zone for zone in zones if zone['zone_type'] == 'slow']

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
    
    class Position:
        @staticmethod
        def is_within_zone(zones, position):
            return Map.Zone.get(zones, position) is not None
        
        # TODO: remove if not used
        #@staticmethod
        #def is_within_city_zone(zones, position, city_id):
        #    zone = Map.Position.get_closest_zone(zones, position)
        #    return Map.Zone.has_city_id(zone, city_id)
        
        @staticmethod
        def get_closest_zone(zones, position):
            """Returns the closest zone to the position."""
            point = Point(position)
            closest_zone = None
            shortest_distance = float('inf') # Initialize to infinity so that the first distance will always be shorter.
            for zone in zones:
                boundary = wkt_loads(zone['boundary'])
                distance = boundary.distance(point)
                if distance < shortest_distance:
                    shortest_distance = distance
                    closest_zone = zone
            return closest_zone