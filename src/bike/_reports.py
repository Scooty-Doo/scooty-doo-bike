from .._utils._clock import Clock
from .._utils._settings import Settings
import math

# TODO: Create a mapper for the reports here or in Brain to output correct JSON format/structure.

class Reports:
    def __init__(self):
        self.reports = []

    def add(self, mode, position, speed, battery_level):
        timestamp = Clock.now()
        self.reports.append({"mode": mode, "position": position, "speed": speed, "timestamp": timestamp, "battery_level": battery_level})
    
    def get(self):
        return self.reports
    
    def last(self):
        return self.reports[-1]
    
    @staticmethod
    def reports_needed(duration) -> int:
        total_reports = math.ceil(duration / Settings.Report.report_interval)
        total_reports = 1 if total_reports == 0 else total_reports
        return total_reports