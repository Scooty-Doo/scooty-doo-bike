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
        self.outgoing = Outgoing(token, bike_id)
        self.running = True

    async def initialize(self):
        if self.bike.zones is None:
            self.bike.zones = await self.request_zones()
        if self.bike.zone_types is None:
            self.bike.zone_types = await self.request_zone_types()

    def _is_not_deployed(self):
        return self.bike.position.current == (
            Settings.Position.default_longitude,
            Settings.Position.default_latitude)

    async def run(self):
        while self.running:
            await self.send_report()
            report_interval = getattr(Settings.Report, f'interval_{self.bike.mode.current}')
            await Clock.sleep(report_interval)

    async def terminate(self):
        self.running = False

    async def send_log(self):
        log = self.bike.logs.last()
        await self.outgoing.logs.send(log)

    async def update_log(self, log=None):
        log = self.bike.logs.last() if not log else log
        await self.outgoing.logs.update(log)

    async def send_logs(self):
        logs = self.bike.logs.get()
        await self.outgoing.logs.send(logs)

    async def send_report(self):
        report = self.bike.reports.last()
        await self.outgoing.reports.send(report)

    async def send_reports(self):
        reports = self.bike.reports.get()
        await self.outgoing.reports.send(reports)

    async def request_zones(self):
        return await self.outgoing.request.zones()

    async def request_zone_types(self):
        return await self.outgoing.request.zone_types()
