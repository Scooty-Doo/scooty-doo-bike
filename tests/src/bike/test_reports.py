"""Tests for the Reports class."""

from src.bike._reports import Reports
from src._utils._format import Format

class TestReports:
    """Tests for the Reports class."""

    def test_initial_reports_empty(self):
        """Test the initial reports are empty."""
        reports = Reports()
        assert not reports.reports

    def test_add_report(self):
        """Test adding a report."""
        reports = Reports()
        report = {"bike_id": 1, "mode": "sleep", "battery_level": 100}
        reports.add(report)
        assert len(reports.reports) == 1
        assert reports.reports[0] == report

    def test_get_reports(self):
        """Test getting reports."""
        reports = Reports()
        report1 = {"bike_id": 1, "mode": "sleep", "battery_level": 100}
        report2 = {"bike_id": 1, "mode": "usage", "battery_level": 95}
        reports.add(report1)
        reports.add(report2)
        formatted = reports.get()
        expected = [Format.report(report1), Format.report(report2)]
        assert formatted == expected

    def test_last_report(self):
        """Test getting the last report."""
        reports = Reports()
        report1 = {"bike_id": 1, "mode": "sleep", "battery_level": 100}
        report2 = {"bike_id": 1, "mode": "usage", "battery_level": 95}
        reports.add(report1)
        reports.add(report2)
        last = reports.last()
        expected = Format.report(report2)
        assert last == expected

    def test_reports_needed_zero(self):
        """Test the number of reports needed with a zero duration."""
        duration = 0
        needed = Reports.reports_needed(duration)
        assert needed == 1
