from ._outgoing import Outgoing
from ..bike.bike import Bike
from .._utils._settings import Settings
from .._utils._clock import Clock

class Brain:
    def __init__(self, bike_id,
                 longitude=None,
                 latitude=None,
                 token=None
                 ):

        self.bike = Bike(bike_id, longitude, latitude)
        self.outgoing = Outgoing(token)
        self.running = True

        if self.bike.zones is None:
            self.bike.zones = self.request_zones()
        if self.bike.zone_types is None:
            self.bike.zone_types = self.request_zone_types()

    def _is_not_deployed(self):
        return self.bike.position.current == (
            Settings.Position.default_longitude,
            Settings.Position.default_latitude)

    def run(self):
        while self.running:
            self.send_report()
            report_interval = getattr(Settings.Report, f'interval_{self.bike.mode.current}')
            Clock.sleep(report_interval)

    def terminate(self):
        self.running = False
        # TODO: clean up _zones.py and _zone_types.py?

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

    def request_zones(self):
        return self.outgoing.request.zones()

    def request_zone_types(self):
        return self.outgoing.request.zone_types()
