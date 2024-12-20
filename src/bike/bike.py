from .._user._user import User
from .._utils._clock import Clock
from .._utils._errors import Errors
from .._utils._map import Map
from .._utils._settings import Settings
from .._utils._route import Route
from ._battery import Battery
from ._position import Position
from ._logs import Logs
from ._reports import Reports
from ._mode import Mode
from ._speed import Speed
from ._city import City
from ._status import Status

class Bike:
    def __init__(self, bike_id,  
                 longitude, 
                 latitude):
        self.bike_id = bike_id
        self.zones = Map.Zones.load()
        self.zone_types = Map.ZoneTypes.load()
        self.battery = Battery()
        self.position = Position(longitude, latitude)
        self.logs = Logs()
        self.reports = Reports()
        self.mode = Mode()
        self.speed = Speed()
        self.user = None
        self.city = City()
        self.city.switch(self.zones, self.position.current)
        if not Map.Position.is_within_zone(self.city.zones, self.position.current):
            self.deploy()
        self.status = Status(self)
        self.report()

    def unlock(self, user_id=None):
        """Unlock the bike."""
        if self.user:
            raise Errors.already_unlocked()
        self.user = User(user_id)
        self.mode.usage()
        self.user.start_trip(self.bike_id, self.position.current)
        trip = self.user.trip
        self.logs.add(trip)
        self.speed.limit(self.city.zones, self.zone_types, self.position.current)
        self.report()

    def lock(self, maintenance=False):
        """Lock the bike."""
        if not self.user and self.mode.is_locked():
            raise Errors.already_locked()
        if not Map.Position.is_within_zone(self.city.zones, self.position.current):
            raise Errors.position_not_within_zone()
        trip = self.user.trip
        self.logs.update(trip)
        self.user.end_trip(self.position.current)
        self.user = None
        self.speed.terminate()
        self.mode.sleep() if not maintenance else self.mode.maintenance()
        self.report()

    def move(self, longitude, latitude):
        """Move the bike to a new position."""
        if not Map.Position.is_within_zone(self.city.zones, (longitude, latitude)):
            raise Errors.out_of_bounds()
        destination = (longitude, latitude)
        current_zone = Map.Zone.get(self.city.zones, self.position.current)
        destination_zone = Map.Zone.get(self.city.zones, destination)
        route = Route.get_route_zones(self.city.zones, current_zone, destination_zone)
        duration = Route.get_duration(self.zone_types, route)
        total_reports = Reports.reports_needed(duration)
        for report_index in range(total_reports):
            self.battery.drain(Settings.Report.report_interval, self.mode.current)
            current_position = Route.get_position(route, total_reports, report_index)
            self.position.change(current_position[0], current_position[1])
            self.speed.limit(self.city.zones, self.zone_types, self.position.current)      
            self.report()
            Clock.sleep(Settings.Report.report_interval)
        route_linestring = Route.get_route_linestring(route)
        self.user.trip.add_route(route_linestring)
        self.logs.update(self.user.trip)
        self.check()

    def relocate(self, longitude, latitude, ignore_zone=True):
        """Relocate the bike to a new position without draining the battery."""
        if not ignore_zone and not Map.Position.is_within_zone(self.zones, (longitude, latitude)):
            raise Errors.out_of_bounds()
        self.position.change(longitude, latitude)
        self.city.switch(self.zones, self.position.current)
        self.speed.limit(self.city.zones, self.zone_types, self.position.current)
        self.report()
    
    def deploy(self):
        """Relocate the bike to a deployment zone."""
        deployment_zone = Map.Zone.get_deployment_zone(self.city.zones)
        deployment_position = Map.Zone.get_centroid_position(deployment_zone)
        self.position.change(deployment_position[0], deployment_position[1])

    def relocate_to_charging_zone(self):
        """Relocate the bike to a charging zone."""
        charging_zone = Map.Zone.get_charging_zone(self.city.zones)
        charging_position = Map.Zone.get_centroid_position(charging_zone)
        self.position.change(charging_position[0], charging_position[1])
        self.speed.limit(self.city.zones, self.zone_types, self.position.current)
        self.report()

    def check(self):
        """Check if the bike needs maintenance."""
        if self.battery.is_low() and self.mode.is_sleep():
            self.mode.maintenance()
            self.report()
        if not Map.Position.is_within_zone(self.city.zones, self.position.current):
            self.mode.maintenance()
            self.report()

    def charge(self, desired_level):
        """Charge the bike to the desired battery level."""
        if not Map.Zone.is_charging_zone(self.city.zones, self.position.current):
            raise Errors.not_charging_zone()
        duration = self.battery.get_charge_time(desired_level)
        total_reports = Reports.reports_needed(duration)
        for _ in range(total_reports):
            self.battery.charge(Settings.Report.report_interval)
            self.report()
            Clock.sleep(Settings.Report.report_interval)

    def report(self):
        """Add a report."""
        self.reports.add(self.status.get(self))

    def update(self, zones=None, zone_types=None):
        """Update the bike's zones and zone types."""
        self.zones = zones if zones else self.zones
        self.zone_types = zone_types if zone_types else self.zone_types
        self.city.switch(self.zones, self.position.current)