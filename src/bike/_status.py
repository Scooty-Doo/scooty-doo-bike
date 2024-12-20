from .._utils._clock import Clock


class Status:
    def __init__(self, bike):
        self.update(bike)

    def update(self, bike):
        self.mode = bike.mode.current
        self.battery_level = bike.battery.level
        self.speed = bike.speed.current
        self.position = bike.position.current
        self.timestamp = Clock.now()

    def get(self, bike):
        self.update(bike)
        return self._format()
    
    def _format(self):
        return self.__dict__
        # TODO: clean up the dictionary and re-format