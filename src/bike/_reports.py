from .._utils._settings import Settings
import math
from shapely.geometry import LineString, Point

# TODO: Create a mapper for the reports here or in Brain to output correct JSON format/structure.

class Reports:
    def __init__(self):
        self.reports = []

    def add(self, status):
        self.reports.append(status)
    
    def get(self):
        return self.reports
    
    def last(self):
        return self.reports[-1]
    
    @staticmethod
    def reports_needed(duration) -> int:
        total_reports = math.ceil(duration / Settings.Report.report_interval)
        total_reports = 1 if total_reports == 0 else total_reports
        return total_reports
    

class ReportMapper:
    @staticmethod
    def map(report):
        ReportMapper._rename(report)
        ReportMapper._remove(report)
        ReportMapper._encode(report)
        return report

    @staticmethod
    def _rename(report):
        if 'position' in report:
            report['last_position'] = report['position']
        if 'battery_level' in report:
            report['battery_lvl'] = report['battery_level']
        if 'bike_id' in report:
            report['id'] = report['bike_id']
    
    @staticmethod
    def _add(report):
        report['is_available'] = True if report['mode'] == 'sleeping' else False
            
    @staticmethod
    def _remove(report):
        if 'timestamp' in report:
            del report['timestamp']
        if 'distance' in report:
            del report['distance']
        # if 'speed' in report: # TODO: speed should be included according to requirements but is not in backend Bike model
        #    del report['speed']
    
    @staticmethod
    def _encode(report):
        if 'path_taken' in report:
            report['path_taken'] = LineString(report['path_taken']).wkt
        if 'start_position' in report:
            report['start_position'] = Point(report['start_position']).wkt
        if 'end_position' in report:
            report['end_position'] = Point(report['end_position']).wkt