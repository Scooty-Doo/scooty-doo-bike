from .bike import Bike
from .._utils._clock import Clock

class Status:
    def __init__(self, bike: Bike):
        self.mode = None
        self.battery_level = None
        self.speed = None
        self.position = None
        self.timestamp = None
        self.update(bike)

    def update(self, bike: Bike):
        self.mode = bike.mode.current()
        self.battery_level = bike.battery.level()
        self.speed = bike.speed.current()
        self.position = bike.position.current()
        self.timestamp = Clock.now()

    def get(self):
        return self.__dict__