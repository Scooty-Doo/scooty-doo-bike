from shapely.geometry import Point, LineString
import math
import json

class Formatter:

    @staticmethod
    def format(entry):
        is_log = Formatter._is_log(entry)
        is_report = Formatter._is_report(entry)
        entry = Formatter._rename(entry, is_log, is_report)
        entry = Formatter._add(entry, is_log, is_report)
        entry = Formatter._remove(entry, is_log, is_report)
        entry = Formatter._encode(entry, is_log, is_report)
        entry = Formatter._format(entry, is_log, is_report)
        return entry

    @staticmethod
    def _is_log(entry):
        return 'route' in entry
    
    @staticmethod
    def _is_report(entry):
        return 'mode' in entry

    @staticmethod
    def _rename(entry, is_log=False, is_report=False):
        if is_log:
            if 'route' in entry:
                entry['path_taken'] = entry.pop('route')
        if is_report:
            if 'position' in entry:
                entry['last_position'] = entry.pop('position')
            if 'battery_level' in entry:
                entry['battery_lvl'] = entry.pop('battery_level')
        return entry

    @staticmethod
    def _add(entry, is_log=False, is_report=False):
        if is_log:
            pass
        if is_report:
            if 'mode' in entry:
                entry['is_available'] = True if entry['mode'] == 'sleeping' else False
                entry.pop('mode')
        return entry

    @staticmethod
    def _remove(entry, is_log=False, is_report=False):
        if is_log:
            if 'duration' in entry:
                del entry['duration']
            if 'distance' in entry:
                del entry['distance']
        if is_report:
            if 'timestamp' in entry:
                del entry['timestamp']
            if 'distance' in entry:
                del entry['distance']
            if 'speed' in entry:
                del entry['speed']
            if 'id' in entry:
                del entry['id']
        return entry

    @staticmethod
    def _encode(entry, is_log=False, is_report=False):
        if is_log:
            if 'path_taken' in entry:
                if entry['path_taken'] is not None and type(entry['path_taken']) is list:
                    if len(entry['path_taken']) > 1:
                        entry['path_taken'] = LineString(entry['path_taken']).wkt
                    else:
                        entry['path_taken'] = None
            if 'start_position' in entry:
                entry['start_position'] = Point(entry['start_position']).wkt
            if 'end_position' in entry:
                entry['end_position'] = Point(entry['end_position']).wkt
        if is_report:
            if 'last_position' in entry:
                entry['last_position'] = Point(entry['last_position']).wkt
        return entry
    
    @staticmethod
    def _format(entry, is_log=False, is_report=False):
        def _remove_space(string):
            return string.replace(" ", "", 1)
        if is_log:
            if 'path_taken' in entry and entry['path_taken'] is not None:
                entry['path_taken'] = _remove_space(entry['path_taken'])
            if 'start_position' in entry:
                entry['start_position'] = _remove_space(entry['start_position'])
            if 'end_position' in entry:
                entry['end_position'] = _remove_space(entry['end_position'])
        if is_report:
            if 'last_position' in entry:
                entry['last_position'] = _remove_space(entry['last_position'])
            if 'battery_lvl' in entry:
                entry['battery_lvl'] = math.ceil(entry['battery_lvl'])
        return entry