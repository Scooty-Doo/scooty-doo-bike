from .._utils._settings import Settings
from .._utils._formatter import Formatter
import math

class Reports:
    def __init__(self):
        self.reports = []

    def add(self, status):
        self.reports.append(status)
    
    def get(self):
        return [Formatter.format(report) for report in self.reports]
    
    def last(self):
        return Formatter.format(self.reports[-1])
    
    @staticmethod
    def reports_needed(duration) -> int:
        total_reports = math.ceil(duration / Settings.Report.report_interval)
        total_reports = 1 if total_reports == 0 else total_reports
        return total_reports