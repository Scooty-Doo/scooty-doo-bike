from .._user._user import User
from .._utils._clock import Clock
from .._utils._map import Map
from .._utils._settings import Settings
from .._utils._validate import Validate
from .._utils._errors import Errors
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
        #if not Map.Position.is_within_zone(self.city.zones, self.position.current):
        #    self.deploy()
        self.status = Status(self)
        self.report()

    def unlock(self, user_id, trip_id):
        """Unlock the bike."""
        if self.user:
            raise Errors.already_unlocked()
        self.user = User(user_id)
        self.mode.usage()
        zone = Map.Zone.get(self.city.zones, self.position.current)
        self.user.start_trip(
            self.bike_id, trip_id, self.position.current,
            zone=zone if zone else None)
        trip = self.user.trip.get()
        self.logs.add(trip)
        self.speed.limit(self.city.zones, self.zone_types, self.position.current)
        self.report()

    def lock(self, maintenance=False, ignore_zone=True):
        """Lock the bike."""
        if not self.user and self.mode.is_locked():
            raise Errors.already_locked()
        if not ignore_zone and not Map.Position.is_within_zone(
            self.city.zones, self.position.current):
            raise Errors.position_not_within_zone()
        zone = Map.Zone.get(self.city.zones, self.position.current)
        self.user.end_trip(self.position.current, zone=zone if zone else None)
        trip = self.user.trip.get()
        self.logs.update(trip)
        self.user.archive_trip()
        self.user = None
        self.speed.terminate()
        if maintenance:
            self.mode.maintenance()
        if not maintenance:
            self.mode.sleep()
        self.report()

    async def move(self, position_or_linestring):
        """Move the bike to a new position or follow a linestring."""
        async def _move(position):
            position = (float(position[0]), float(position[1])) # TODO: can be removed?
            speed_in_kmh = self.speed.default
            distance_in_km = Map.Position.get_distance_in_km(self.position.current, position)
            total_duration_in_minutes = Clock.get_duration_in_minutes(distance_in_km, speed_in_kmh)
            total_reports = Reports.reports_needed(total_duration_in_minutes)
            for report_index in range(total_reports):
                report_interval_in_minutes = Clock.convert_seconds_to_minutes(
                    Settings.Report.interval)
                minutes_travelled = report_interval_in_minutes * (report_index + 1)
                self.battery.drain(report_interval_in_minutes, self.mode.current)
                current_position = Map.Position.get_position_after_minutes_travelled(
                    self.position.current, position, minutes_travelled, speed_in_kmh)
                self.position.change(current_position[0], current_position[1])
                self.speed.limit(self.city.zones, self.zone_types, self.position.current)
                self.report()
                leg_duration_in_seconds = Clock.get_leg_duration_in_seconds(
                    total_duration_in_minutes, total_reports)
                await Clock.sleep(leg_duration_in_seconds)
            self.user.trip.add_movement(self.position.current)
            self.logs.update(self.user.trip.get())
            self.check()
            self.mode.submodes.usage.moving = False
        if self.mode.is_locked():
            raise Errors.already_locked()
        if Position.is_position(position_or_linestring):
            self.mode.submodes.usage.moving = True
            await _move(position_or_linestring)
            self.mode.submodes.usage.moving = False
        elif Validate.is_linestring(position_or_linestring):
            self.mode.submodes.usage.moving = True
            for position in position_or_linestring:
                await _move(position)
            self.mode.submodes.usage.moving = False
        elif not Position.is_position(position_or_linestring) \
            or not Validate.is_linestring(position_or_linestring):
            Validate.position_or_linestring(position_or_linestring)

    def relocate(self, position, ignore_zone=True):
        """Relocate the bike to a new position without draining the battery."""
        if not ignore_zone and not Map.Position.is_within_zone(self.zones, position):
            raise Errors.out_of_bounds()
        if not Position.is_position(position):
            Validate.position(position)
        self.position.change(position[0], position[1])
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

    def check(self, maintenance=False):
        """Check if the bike needs maintenance."""
        if maintenance: # TODO: if this one is used a trip should be ended gracefully in some way...
            self.mode.maintenance()
            self.report()
            return
        if self.battery.is_low() and self.mode.is_sleep():
            self.mode.maintenance()
            self.report()
        if not Map.Zone.has_city_id(
            Map.Position.get_closest_zone(self.city.zones, self.position.current), self.city.id):
            self.mode.maintenance()
            self.report()
            raise Errors.out_of_bounds()

    async def charge(self, desired_level):
        """Charge the bike to the desired battery level."""
        if not Map.Zone.is_charging_zone(self.city.zones, self.position.current):
            raise Errors.not_charging_zone()
        self.mode.submodes.usage.charging = True
        total_duration_in_minutes = self.battery.get_charge_time(desired_level)
        total_reports = Reports.reports_needed(total_duration_in_minutes)
        for _ in range(total_reports):
            self.battery.charge(Clock.convert_seconds_to_minutes(Settings.Report.interval))
            self.report()
            leg_duration_in_seconds = Clock.get_leg_duration_in_seconds(
                total_duration_in_minutes, total_reports)
            await Clock.sleep(leg_duration_in_seconds)
        self.mode.submodes.usage.charging = False

    def report(self):
        """Add a report."""
        self.reports.add(self.status.get(self))

    def update(self, zones=None, zone_types=None):
        """Update the bike's zones and zone types."""
        self.zones = zones if zones else self.zones
        self.zone_types = zone_types if zone_types else self.zone_types
        self.city.switch(self.zones, self.position.current)

    def is_moving_or_charging(self):
        """Check if the bike is moving or charging."""
        return self.mode.submodes.usage.moving or self.mode.submodes.usage.charging
