# TODO: ta bort

# from shapely.geometry import LineString
# from shapely.wkt import loads as wkt_loads
# import math

# class Route:

#     @staticmethod
#     def get_route_zones(zones, start_zone, end_zone):
#         start_centroid = wkt_loads(start_zone['boundary']).centroid
#         end_centroid = wkt_loads(end_zone['boundary']).centroid
#         route = LineString([start_centroid, end_centroid])
#         intersecting_zones = []
#         for zone in zones:
#             boundary = wkt_loads(zone['boundary'])
#             if route.intersects(boundary):
#                 intersecting_zones.append(zone)
#         sorted_zones = sorted(intersecting_zones, key=lambda zone: route.project(wkt_loads(zone['boundary']).centroid))
#         return sorted_zones

#     @staticmethod
#     def get_route_linestring(route):
#         linestring = []
#         for zone in route:
#             boundary = wkt_loads(zone['boundary'])
#             centroid = boundary.centroid
#             linestring.append((centroid.x, centroid.y))
#         return linestring
    
#     @staticmethod
#     def get_duration(zone_types, route):
#         if len(route) < 2:
#             return 0
#         total_minutes = 0
#         for current_zone_index in range(len(route) - 1):
#             current_zone = route[current_zone_index]
#             next_zone = route[current_zone_index + 1]
#             current_centroid = wkt_loads(current_zone['boundary']).centroid
#             next_centroid = wkt_loads(next_zone['boundary']).centroid
#             distance = Route._get_distance(current_centroid, next_centroid)
#             speed = zone_types[current_zone['zone_type']]['speed_limit']
#             hours = distance / speed
#             minutes = hours * 60
#             total_minutes += minutes
#         return int(total_minutes)
    
#     @staticmethod
#     def _get_distance(current_centroid, next_centroid):
#         return current_centroid.distance(next_centroid) / 1000
    
#     @staticmethod
#     def get_position(route, total_reports, report_index):
#         zone_count = len(route)
#         if zone_count == 1:
#             centroid = wkt_loads(route[0]['boundary']).centroid
#             return (centroid.x, centroid.y)
#         step_size = total_reports // zone_count
#         zone_index = math.ceil(step_size * report_index)
#         zone_index = min(zone_index, zone_count - 1)
#         zone = route[zone_index]
#         centroid = wkt_loads(zone['boundary']).centroid
#         return (centroid.x, centroid.y)

