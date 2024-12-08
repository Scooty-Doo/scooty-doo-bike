from ._map import Map
from geopy.distance import geodesic
# TODO: Can use a simpler calculation since city travel.
# TODO: But need to know how coordinates/position looks?

class Route:
    def __init__(self):
        pass

    # Route defined as a list of distance-speed pairs.
    # TODO: understand the zone structure (boundary etc.)
    # TODO: then implement the rest
    # NOTE: atm no way to get speed limit for zone from REST API?

    def get_route(self, zones, position, destination):
        route = []
        current_position = position
        while current_position != destination:
            speed = Map.Zone.speed_limit(zones, current_position)
            next_zone = self._calculate_next_zone(current_position, destination)
            if not next_zone:
                break
            start_of_next_zone = next_zone[0]
            distance = self._get_distance(current_position, start_of_next_zone)
            leg = (distance, speed)
            route.append(leg)
            current_position = start_of_next_zone
        final_distance = self._get_distance(current_position, destination)
        final_speed = Map.Zone.get(zones, destination).speed_limit
        final_leg = (final_distance, final_speed)
        route.append(final_leg)
        return route
    
    def _calculate_next_zone(self):
        pass

    def _get_distance(self, position, destination):
        return int(geodesic(position, destination).meters)
    
    def _get_route_time(self, route):
        pass

    def _get_battery_time(self):
        pass
    
    def premature_end(self, route, battery_level):
        route_time = self._get_route_time(route)
        battery_time = self._get_battery_time()
        if route_time < battery_time:
            return
        # calculate position after X minutes en route.
