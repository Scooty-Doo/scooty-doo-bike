from .._utils._clock import Clock
from .._utils._settings import Settings
import math

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
    
    @staticmethod
    def calculate_total_reports_in_duration(duration):
        total_reports = math.ceil(duration / Settings.Report.report_interval)
        total_reports = 1 if total_reports == 0 else total_reports
        return total_reports