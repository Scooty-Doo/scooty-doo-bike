from .._utils._formatter import Formatter

class Logs:
    def __init__(self):
        self.logs = []

    def add(self, trip):
        log = Formatter.format(trip.__dict__)
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