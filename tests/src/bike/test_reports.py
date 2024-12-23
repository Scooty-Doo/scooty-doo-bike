from src.bike._reports import Reports
from src._utils._settings import Settings
from src._utils._format import Format

class TestReports:

    def test_initial_reports_empty(self):
        reports = Reports()
        assert reports.reports == []

    def test_add_report(self):
        reports = Reports()
        report = {"bike_id": 1, "mode": "sleep", "battery_level": 100}
        reports.add(report)
        assert len(reports.reports) == 1
        assert reports.reports[0] == report

    def test_get_reports(self):
        reports = Reports()
        report1 = {"bike_id": 1, "mode": "sleep", "battery_level": 100}
        report2 = {"bike_id": 1, "mode": "usage", "battery_level": 95}
        reports.add(report1)
        reports.add(report2)
        formatted = reports.get()
        expected = [Format._apply_all_formatting(report1), Format._apply_all_formatting(report2)]
        assert formatted == expected

    def test_last_report(self):
        reports = Reports()
        report1 = {"bike_id": 1, "mode": "sleep", "battery_level": 100}
        report2 = {"bike_id": 1, "mode": "usage", "battery_level": 95}
        reports.add(report1)
        reports.add(report2)
        last = reports.last()
        expected = Format._apply_all_formatting(report2)
        assert last == expected

    def test_reports_needed_zero(self):
        duration = 0
        needed = Reports.reports_needed(duration)
        assert needed == 1
