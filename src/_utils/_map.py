import random
import json
import os
from shapely.geometry import Point
from shapely.wkt import loads as wkt_loads

ZONES_FILENAME = '_zones.json'
ZONE_TYPES_FILENAME = '_zone_types.json'

# TODO: Kolla på att optimisera användandet av zoner (se Martins kommentar i Discord).

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

        @staticmethod
        def has_city_id(zone, city_id):
            return Map.Zone.get_city_id(zone) == city_id

        @staticmethod
        def get_city_id(zone):
            return zone['city_id']

        @staticmethod
        def get_zone_id(zone):
            return zone['id']

        @staticmethod
        def get_zone_type(zone):
            return zone['zone_type']

        @staticmethod
        def get_centroid_position(zone):
            """Returns the centroid of the zone."""
            boundary = wkt_loads(zone['boundary'])
            return (boundary.centroid.x, boundary.centroid.y)

        @staticmethod
        def get_speed_limit(zones, zone_types, position):
            zone = Map.Zone.get(zones, position)
            zone = zone if zone else Map.Position.get_closest_zone(zones, position)
            zone_type = Map.Zone.get_zone_type(zone)
            speed_limit = zone_types[zone_type]['speed_limit']
            return speed_limit

        @staticmethod
        def is_charging_zone(zones, position):
            zone = Map.Zone.get(zones, position)
            if Map.Zone.get_zone_type(zone) == 'charging':
                return True
            return False

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
            with open(file=file_path, mode='r', encoding='utf-8') as f:
                zones = json.load(f)
                if not zones:
                    return []
            return zones

        @staticmethod
        def get_zones_with_city_id(zones, city_id):
            return [zone for zone in zones if Map.Zone.get_city_id(zone) == city_id]

        @staticmethod
        def get_parking_zones(zones):
            return [zone for zone in zones if Map.Zone.get_zone_type(zone) == 'parking']

        @staticmethod
        def get_charging_zones(zones):
            return [zone for zone in zones if Map.Zone.get_zone_type(zone) == 'charging']

    class ZoneTypes:
        @staticmethod
        def load():
            current_directory = os.path.dirname(__file__)
            file_path = os.path.join(current_directory, ZONE_TYPES_FILENAME)
            with open(file=file_path, mode='r', encoding='utf-8') as f:
                zone_types = json.load(f)
                if not zone_types:
                    return {}
            return zone_types

    class Position:
        @staticmethod
        def is_within_zone(zones, position):
            return Map.Zone.get(zones, position) is not None

        @staticmethod
        def get_closest_zone(zones, position):
            """Returns the closest zone to the position."""
            point = Point(position)
            closest_zone = None
             # Initialize to infinity so that the first distance will always be shorter.
            shortest_distance = float('inf')
            for zone in zones:
                boundary = wkt_loads(zone['boundary'])
                distance = boundary.distance(point)
                if distance < shortest_distance:
                    shortest_distance = distance
                    closest_zone = zone
            return closest_zone

        @staticmethod
        def get_distance_in_km(start_position, end_position):
            def _convert_to_kilometers(distance):
                return distance / 1000
            start_point = Point(start_position)
            end_point = Point(end_position)
            distance = start_point.distance(end_point)
            return _convert_to_kilometers(distance)

        @staticmethod
        def get_position_after_minutes_travelled(
            start_position, end_position,
            minutes_travelled, speed
            ):

            def _get_distance_travelled(speed, minutes_travelled):
                return speed * (minutes_travelled / 60)

            def _calculate_fraction_of_distance_travelled(distance_travelled, distance):
                return distance_travelled / distance

            def _calculate_final_position(
                    start_position, end_position,
                    distance_travelled, distance
                    ):

                fraction_of_distance_travelled = \
                    _calculate_fraction_of_distance_travelled(
                        distance_travelled, distance)

                x1, y1 = start_position
                x2, y2 = end_position
                x = x1 + (x2 - x1) * fraction_of_distance_travelled
                y = y1 + (y2 - y1) * fraction_of_distance_travelled
                return (x, y)

            distance = Map.Position.get_distance_in_km(start_position, end_position)
            distance_travelled = _get_distance_travelled(speed, minutes_travelled)

            if distance_travelled >= distance:
                return end_position

            return _calculate_final_position(start_position, end_position,
                                             distance_travelled, distance
                                             )
