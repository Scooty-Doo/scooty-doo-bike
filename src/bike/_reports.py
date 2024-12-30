import math
from .._utils._settings import Settings
from .._utils._format import Format

class Reports:
    def __init__(self):
        self.reports = []

    def add(self, status):
        self.reports.append(status)

    def get(self):
        return [Format.report(report) for report in self.reports]

    def last(self):
        return Format.report(self.reports[-1])

    @staticmethod
    def reports_needed(duration_in_minutes) -> int:
        total_reports = math.ceil(duration_in_minutes / (Settings.Report.interval / 60))
        total_reports = 1 if total_reports == 0 else total_reports
        return total_reports
