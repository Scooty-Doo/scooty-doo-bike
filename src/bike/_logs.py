from shapely import LineString, Point

class Logs:
    def __init__(self):
        self.logs = []

    def add(self, trip):
        log = LogMapper.map(trip.__dict__)
        if self._exists(log):
            index = self._get_log_index(log)
            self.logs[index] = log
        else:
            self.logs.append(log)
    
    def update(self, trip):
        self.add(trip)

    def get(self):
        return self.logs
    
    def last(self):
        return self.logs[-1]

    def _exists(self, log):
        return any([log["id"] == entry["id"] for entry in self.logs])

    def _get_log_index(self, log):
        return [log["id"] == entry["id"] for entry in self.logs].index(True)


class LogMapper:

    @staticmethod
    def map(log):
        LogMapper._rename(log)
        LogMapper._remove(log)
        LogMapper._encode_as_wkt(log)
        return log

    @staticmethod
    def _rename(log):
        if 'route' in log:
            log['path_taken'] = log['route']

    @staticmethod
    def _remove(log):
        if 'duration' in log:
            del log['duration']
        if 'distance' in log:
            del log['distance']
    
    @staticmethod
    def _encode_as_wkt(log):
        if 'path_taken' in log:
            log['path_taken'] = LineString(log['path_taken']).wkt
        if 'start_position' in log:
            log['start_position'] = Point(log['start_position']).wkt
        if 'end_position' in log:
            log['end_position'] = Point(log['end_position']).wkt