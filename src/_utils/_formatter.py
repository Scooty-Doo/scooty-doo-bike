from shapely.geometry import Point, LineString

class Formatter:

    @staticmethod
    def format(entry):
        Formatter._rename(entry)
        Formatter._add(entry)
        Formatter._remove(entry)
        Formatter._encode(entry)
        Formatter._format(entry)
        return entry

    @staticmethod
    def _rename(entry):
        # LOG
        if 'route' in entry:
            entry['path_taken'] = entry.pop('route')
        # REPORT
        if 'position' in entry:
            entry['last_position'] = entry.pop('position')
        if 'battery_level' in entry:
            entry['battery_lvl'] = entry.pop('battery_level')

    @staticmethod
    def _add(entry):
        # REPORT
        if 'mode' in entry:
            entry['is_available'] = True if entry['mode'] == 'sleeping' else False
            entry.pop('mode')

    @staticmethod
    def _remove(entry):
        # LOG
        if 'duration' in entry:
            del entry['duration']
        if 'distance' in entry:
            del entry['distance']

        # REPORT   
        if 'timestamp' in entry:
            del entry['timestamp']
        if 'distance' in entry:
            del entry['distance']
        if 'speed' in entry:
            del entry['speed']

    @staticmethod
    def _encode(entry):
        if 'path_taken' in entry:
            entry['path_taken'] = LineString(entry['path_taken']).wkt
        if 'start_position' in entry:
            entry['start_position'] = Point(entry['start_position']).wkt
        if 'end_position' in entry:
            entry['end_position'] = Point(entry['end_position']).wkt
        if 'last_position' in entry:
            entry['last_position'] = Point(entry['last_position']).wkt
    
    @staticmethod
    def _format(entry):
        def _remove_space(string):
            return string.replace(" ", "", 1)
        if 'path_taken' in entry:
            entry['path_taken'] = _remove_space(entry['path_taken'])
        if 'start_position' in entry:
            entry['start_position'] = _remove_space(entry['start_position'])
        if 'end_position' in entry:
            entry['end_position'] = _remove_space(entry['end_position'])
        if 'last_position' in entry:
            entry['last_position'] = _remove_space(entry['last_position'])