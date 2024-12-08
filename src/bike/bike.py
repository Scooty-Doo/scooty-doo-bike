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
        self.user = User(user_id)           # Create a User
        self.mode.usage()                   # Set the mode to 'usage'
        self.user.start_trip(self.bike_id, self.position.current)  # Start a trip for the user
        trip = self.user.trip               # Get the trip object
        self.logs.add(trip)                  # Log the trip
        self.speed.limit(self.zones, self.position.current)                  # Set speed to speed limit
        self.reports.add(self.mode.current, self.position.current, self.speed.current)

    def lock(self, ignore_zone=False, maintenance=False):
        """Locks the bike."""
        if not self.user and self.mode.is_locked(): # Verify not already locked
            raise Errors.already_locked()
        if not Map.Zone.is_parking_zone(self.zones, self.position.current) and not ignore_zone:  # Verify zone
            raise Errors.not_parking_zone()
        trip = self.user.trip                       # Get the trip object
        self.logs.update(trip)                       # Update the trip log
        self.user.end_trip(self.position.current)   # End the trip for the user
        self.speed.terminate()                      # Set speed to 0
        self.mode.sleep() if not maintenance else self.mode.maintenance() # Select mode
        self.report()

    def move(self, longitude, latitude):
        """Updates the bike's position."""
        destination = (longitude, latitude)
        route = Route.get_route(self.zones, self.position.current, destination)
        
        while self.battery.level > 0 and route:
            leg = route.pop(0)
            distance, speed = leg
            minutes = distance / speed # tune in minutes
            self.battery.drain(minutes, self.mode.current)

        #actual_destination = last_position
        # calculate total time or change battery consumption to distance instead of time?
        # but then maybe no simple simulation speed up?
        #self.position.change(actual_destination[0], actual_destination[1])
        self.speed.limit(self.zones, self.position.current)       
        self.report()

    def relocate(self, longitude, latitude):
        """Relocate the bike to a new position."""
        self.position.change(longitude, latitude)
        self.speed.limit(self.zones, self.position.current)
        self.report()
        # ... except no battery drain
    
    def deploy(self, parking_zones):
        deployment_zone = Map.Zone.get_deployment_zone(parking_zones)
        deployment_position = None # TODO: get a position within the deployment zone
        self.position.change(deployment_position[0], deployment_position[1])


    def check(self):
        # Check if bike needs maintenance
        if self.battery.is_low() and self.mode.is_sleep():
            self.mode.maintenance()
            self.report()
        # check if bike needs to be relocated --> maintenance

    def charge(self, desired_level):
        if not Map.Zone.is_charging_zone(self.zones, self.position.current):
            raise Errors.not_charging_zone()
        minutes_spent = self.battery.charge(desired_level)
        self.report()
        return minutes_spent

    def report(self):
        self.reports.add(self.mode.current, self.position.current, self.speed.current)

    def update(self, zones):
        self.zones = zones