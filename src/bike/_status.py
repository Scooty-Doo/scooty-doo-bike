from .._utils._clock import Clock
import copy

class Status:
    def __init__(self, bike):
        self.update(bike)

    def update(self, bike):
        self.id = bike.bike_id
        self.mode = bike.mode.current
        self.battery_level = bike.battery.level
        self.speed = bike.speed.current
        self.position = bike.position.current
        self.timestamp = Clock.now()
        self.city_id = bike.city.id

    def get(self, bike):
        self.update(bike)
        return copy.deepcopy(self.__dict__)