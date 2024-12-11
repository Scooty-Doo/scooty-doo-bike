from shapely.geometry import Point, Polygon

import json
import os

ZONES_FILENAME = '_zones.json'
PARKING_ZONES_FILENAME = '_parking_zones.json'

# _zones.json
# [
#     {
#         "id": 1,
#         "zone_name": "zone1",
#         "zone_type": "parking",
#         "city": "city1",
#         "boundary": ""
#     },
# ]

class Map:
    class Zone:
        @staticmethod
        def get(zones, position):
            # TODO: implement correctly
            point = Point(position)
            for zone in zones:
                boundary = None # TODO: how does boundary work?
                if point.within(boundary):
                    return zone 
        
        def speed_limit(zones, position):
            zone = Map.Zone.get(zones, position)
            if zone:
                return zone['speed_limit'] # TODO: match actual structure
            return 0

        @staticmethod
        def is_parking_zone(parking_zones, position):
            zone = Map.Zone.get(parking_zones, position)
            if zone and zone in parking_zones:
                return True
            pass

        @staticmethod
        def is_charging_zone(parking_zones, position):
            zone = Map.Zone.get(parking_zones, position)
            if zone and zone in parking_zones:
                return True
            
        @staticmethod
        def get_deployment_zone(parking_zones):
            # TODO: pick a parking zone at random and return it
            pass

    class Zones:
        @staticmethod
        def load():
            current_directory = os.path.dirname(__file__)
            file_path = os.path.join(current_directory, ZONES_FILENAME)
            with open(file_path) as f:
                zones = json.load(f)
            return zones
    
        class Parking:
            @staticmethod
            def load():
                current_directory = os.path.dirname(__file__)
                file_path = os.path.join(current_directory, PARKING_ZONES_FILENAME)
                with open(file_path) as f:
                    zones = json.load(f)
                return zones