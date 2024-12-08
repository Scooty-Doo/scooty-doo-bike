from ._outgoing import Outgoing
from ..bike.bike import Bike
from .._utils._settings import Settings
import time

class Brain:
    def __init__(self, bike_id,  
                 longitude, latitude, 
                 token=None,
                 zones=None,
                 ):
        self.bike = Bike(bike_id, longitude, latitude, zones)
        self.outgoing = Outgoing(token)
        self.running = True
        self.settings = Settings.ReportSettings()

    def run(self):
        while self.running:
            self.send_report()
            time.sleep(self.settings.report_interval)
    
    def terminate(self):
        self.running = False

    def send_log(self):
        log = self.bike.logs.last()
        self.outgoing.logs.send(log)

    def update_log(self, log=None):
        log = self.bike.logs.last() if not log else log
        self.outgoing.logs.update(log)
    
    def send_logs(self):
        logs = self.bike.logs.get()
        self.outgoing.logs.send(logs)

    def send_report(self):
        report = self.bike.reports.last()
        self.outgoing.reports.send(report)
    
    def send_reports(self):
        reports = self.bike.reports.get()
        self.outgoing.reports.send(reports)
