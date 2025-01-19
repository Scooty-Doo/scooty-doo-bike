# pylint: disable=too-few-public-methods
"""
Module for handling logic related to the map and its zones.
"""

import random
import json
import os
from shapely.geometry import Point
from shapely.wkt import loads as wkt_loads

ZONES_FILENAME = '_zones.json'
ZONE_TYPES_FILENAME = '_zone_types.json'

class Map:
    """Class handling logic related to the map and its zones."""
    class Zone:
        """Class handling logic related to dealing with individual zones."""
        @staticmethod
        def get(zones, position):
            """Returns the zone that covers the position."""
            point = Point(position)
            for zone in zones:
                boundary = wkt_loads(zone['boundary'])
                if boundary.covers(point):
                    return zone
            return None

        @staticmethod
        def has_city_id(zone, city_id):
            """Returns True if the zone has the city_id."""
            return Map.Zone.get_city_id(zone) == city_id

        @staticmethod
        def get_city_id(zone):
            """Returns the city_id of the zone."""
            return zone['city_id']

        @staticmethod
        def get_zone_id(zone):
            """Returns the id of the zone."""
            return zone['id']

        @staticmethod
        def get_zone_type(zone):
            """Returns the zone type of the zone."""
            return zone['zone_type']

        @staticmethod
        def get_centroid_position(zone):
            """Returns the centroid of the zone."""
            boundary = wkt_loads(zone['boundary'])
            return (boundary.centroid.x, boundary.centroid.y)

        @staticmethod
        def get_speed_limit(zones, zone_types, position):
            """Returns the speed limit of the zone that covers the position."""
            zone = Map.Zone.get(zones, position)
            zone = zone if zone else Map.Position.get_closest_zone(zones, position)
            zone_type = Map.Zone.get_zone_type(zone)
            speed_limit = zone_types[zone_type]['speed_limit']
            return speed_limit

        @staticmethod
        def is_charging_zone(zones, position):
            """Returns True if the position is within a charging zone."""
            zone = Map.Zone.get(zones, position)
            if Map.Zone.get_zone_type(zone) == 'charging':
                return True
            return False

        @staticmethod
        def get_deployment_zone(zones):
            """Returns a random deployment zone."""
            parking_zones = Map.Zones.get_parking_zones(zones)
            random_parking_zone = random.choice(parking_zones)
            return random_parking_zone

        @staticmethod
        def get_charging_zone(zones):
            """Returns a random charging zone."""
            charging_zones = Map.Zones.get_charging_zones(zones)
            random_charging_zone = random.choice(charging_zones)
            return random_charging_zone

    class Zones:
        """Class handling logic related handling multiple zones."""

        @staticmethod
        def load():
            """Loads the zones from the file."""
            current_directory = os.path.dirname(__file__)
            file_path = os.path.join(current_directory, ZONES_FILENAME)
            with open(file=file_path, mode='r', encoding='utf-8') as f:
                zones = json.load(f)
                if not zones:
                    return []
            return zones

        @staticmethod
        def get_zones_with_city_id(zones, city_id):
            """Returns the zones with the city_id."""
            return [zone for zone in zones if Map.Zone.get_city_id(zone) == city_id]

        @staticmethod
        def get_parking_zones(zones):
            """Returns the parking zones."""
            return [zone for zone in zones if Map.Zone.get_zone_type(zone) == 'parking']

        @staticmethod
        def get_charging_zones(zones):
            """Returns the charging zones."""
            return [zone for zone in zones if Map.Zone.get_zone_type(zone) == 'charging']

    class ZoneTypes:
        """Class handling logic related to the zone types."""
        @staticmethod
        def load():
            """Loads the zone types from the file."""
            current_directory = os.path.dirname(__file__)
            file_path = os.path.join(current_directory, ZONE_TYPES_FILENAME)
            with open(file=file_path, mode='r', encoding='utf-8') as f:
                zone_types = json.load(f)
                if not zone_types:
                    return {}
            return zone_types

    class Position:
        """Class handling logic related to positions on the map."""
        @staticmethod
        def is_within_zone(zones, position):
            """Returns True if the position is within a zone."""
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
            """Returns the distance in kilometers between two positions."""
            def _convert_to_kilometers(distance):
                """Converts a distance to kilometers."""
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
            """Returns the position after minutes travelled at a certain speed."""

            def _get_distance_travelled(speed, minutes_travelled):
                """Returns the distance travelled."""
                return speed * (minutes_travelled / 60)

            def _calculate_fraction_of_distance_travelled(distance_travelled, distance):
                """Returns the fraction of the distance travelled."""
                return distance_travelled / distance

            def _calculate_final_position(
                    start_position, end_position,
                    distance_travelled, distance
                    ):
                """Returns the final position."""

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
