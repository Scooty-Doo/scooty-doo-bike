from .._utils._clock import Clock

class Reports:
    def __init__(self):
        self.reports = []

    def add(self, mode, position, speed):
        timestamp = Clock.now()
        self.reports.append({"mode": mode, "position": position, "speed": speed, "timestamp": timestamp})
    
    def get(self):
        return self.reports
    
    def last(self):
        return self.reports[-1]