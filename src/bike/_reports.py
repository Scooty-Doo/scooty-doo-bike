"""
Module for the Reports class.
"""

import math
from .._utils._settings import Settings
from .._utils._format import Format

class Reports:
    """Class handling the reports of the bike."""
    def __init__(self):
        self.reports = []

    def add(self, status):
        """Add a report entry."""
        self.reports.append(status)

    def get(self):
        """Return all reports."""
        return [Format.report(report) for report in self.reports]

    def last(self):
        """Return the last report."""
        return Format.report(self.reports[-1])

    @staticmethod
    def reports_needed(duration_in_minutes) -> int:
        """Get the number of reports needed for a certain duration."""
        total_reports = math.ceil(duration_in_minutes / (Settings.Report.interval / 60))
        total_reports = 1 if total_reports == 0 else total_reports
        return total_reports
