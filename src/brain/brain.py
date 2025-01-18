"""
This module adds incoming and outgoing communication to the bike object.
This enables it to communicate with the backend.
"""

from random import randint
import logging
import httpx
from ._outgoing import Outgoing
from ..bike.bike import Bike
from .._utils._settings import Settings
from .._utils._clock import Clock

class Brain:
    """
    Class representing a bike brain, which handles all the bike behavior 
    as well as incoming and outgoing communication.
    """
    def __init__(self, bike_id,
                 longitude=None,
                 latitude=None,
                 token=None
                 ):

        self.bike = Bike(bike_id, longitude, latitude)
        self.outgoing = Outgoing(token, bike_id)
        self.running = True
        self.logger = logging.getLogger(__name__)

    async def initialize(self):
        """Initialize the bike brain with zones and zone types."""
        if self.bike.zones is None:
            self.bike.zones = await self.request_zones()
        if self.bike.zone_types is None:
            self.bike.zone_types = await self.request_zone_types()

    def is_not_deployed(self):
        """Check if the bike is not deployed."""
        return self.bike.position.current == (
            Settings.Position.default_longitude,
            Settings.Position.default_latitude)

    async def run(self):
        """Run the bike brain."""
        while self.running:
            report_interval = getattr(Settings.Report, f'interval_{self.bike.mode.current}')
            delay = randint(report_interval, 1000)
            wait_time = report_interval + (delay/1000)
            await Clock.sleep(wait_time)
            try:
                await self.send_report()
            except httpx.HTTPStatusError as e:
                self.logger.error("HTTPStatusError while sending report: %s", e)
                print(f"HTTPStatusError while sending report: {e}")
                raise
            except Exception as e:
                self.logger.error("Unexpected error while sending report: %s", e)
                print(f"Unexpected error while sending report: {e}")
                raise

    async def terminate(self):
        """Terminate the bike brain."""
        self.running = False

    async def send_log(self):
        """Send the last log."""
        log = self.bike.logs.last()
        await self.outgoing.logs.send(log)

    async def update_log(self, log=None):
        """Update the log."""
        log = self.bike.logs.last() if not log else log
        await self.outgoing.logs.update(log)

    async def send_logs(self):
        """Send all logs."""
        logs = self.bike.logs.get()
        await self.outgoing.logs.send(logs)

    async def send_report(self):
        """Send the last report."""
        report = self.bike.reports.last()
        await self.outgoing.reports.send(report)

    async def send_reports(self):
        """Send all reports."""
        reports = self.bike.reports.get()
        await self.outgoing.reports.send(reports)

    async def request_zones(self):
        """Request all zones from the backend."""
        return await self.outgoing.request.zones()

    async def request_zone_types(self):
        """Request all zone types from the backend."""
        return await self.outgoing.request.zone_types()
