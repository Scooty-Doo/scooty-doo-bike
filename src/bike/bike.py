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

class Bike:
    def __init__(self, bike_id,  
                 longitude, 
                 latitude):
        self.bike_id = bike_id
        self.zones = Map.Zones.load()
        self.zone_types = Map.ZoneTypes.load()
        self.parking_zones = Map.Zones.get_parking_zones(self.zones)
        self.battery = Battery()
        self.position = Position(longitude, latitude)
        self.logs = Logs()
        self.reports = Reports()
        self.mode = Mode()
        self.speed = Speed()
        self.user = None
        self.report()

    def unlock(self, user_id=None):
        """User unlocks the bike and can start using it."""
        if self.user:
            raise Errors.already_unlocked()
        self.user = User(user_id)
        self.mode.usage()
        self.user.start_trip(self.bike_id, self.position.current)
        trip = self.user.trip
        self.logs.add(trip)
        self.speed.limit(self.zones, self.position.current)
        self.reports.add(self.mode.current, self.position.current, self.speed.current)

    def lock(self, ignore_zone=False, maintenance=False):
        """Locks the bike."""
        if not self.user and self.mode.is_locked():
            raise Errors.already_locked()
        if not Map.Zone.is_parking_zone(self.zones, self.position.current) and not ignore_zone:
            raise Errors.not_parking_zone()
        trip = self.user.trip
        self.logs.update(trip)
        self.user.end_trip(self.position.current)
        self.speed.terminate()
        self.mode.sleep() if not maintenance else self.mode.maintenance()
        self.report()

    def move(self, longitude, latitude):
        """Updates the bike's position."""
        destination = (longitude, latitude)
        current_zone = Map.Zone.get(self.zones, self.position.current)
        destination_zone = Map.Zone.get(self.zones, destination)
        route = Route.get(self.zones, current_zone, destination_zone)
        duration = Route.get_duration(self.zone_types, route)
        total_reports = Reports.calculate_total_reports_in_duration(duration)
        for report_index in range(total_reports):
            self.battery.drain(Settings.Report.report_interval, self.mode.current)
            current_position = Route.get_position(route, total_reports, report_index)
            self.position.change(current_position[0], current_position[1])
            self.speed.limit(self.zones, self.position.current)      
            self.report()
            Clock.sleep(Settings.Report.report_interval)
        self.check() 

    def relocate(self, longitude, latitude):
        """Relocate the bike to a new position without draining the battery."""
        self.position.change(longitude, latitude)
        self.speed.limit(self.zones, self.position.current)
        self.report()
    
    def deploy(self):
        deployment_zone = Map.Zone.get_deployment_zone(self.zones)
        deployment_position = Map.Zone.get_position(deployment_zone)
        self.position.change(deployment_position[0], deployment_position[1])

    def check(self):
        if self.battery.is_low() and self.mode.is_sleep():
            self.mode.maintenance()
            self.report()

    def charge(self, desired_level):
        if not Map.Zone.is_charging_zone(self.zones, self.position.current):
            raise Errors.not_charging_zone()
        duration = self.battery.get_charge_time(desired_level)
        total_reports = Reports.calculate_total_reports_in_duration(duration)
        for _ in range(total_reports):
            self.battery.charge(Settings.Report.report_interval)
            self.report()
            Clock.sleep(Settings.Report.report_interval)

    def report(self):
        self.reports.add(self.mode.current, self.position.current, self.speed.current)

    def update(self, zones=None, zone_types=None):
        self.zones = zones if zones else self.zones
        self.zone_types = zone_types if zone_types else self.zone_types