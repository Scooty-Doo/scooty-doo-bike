from .._utils._errors import Errors
from .._utils._settings import Settings
import math

class Battery:
    def __init__(self, battery_level=100.0):
        self.level = battery_level
        self.settings = Settings.Battery()

    def update(self, settings):
        for key, value in settings.__dict__.items():
            setattr(self, key, value)
        
    def get_charge_time(self, desired_level=100.0):
        charging_left = desired_level - self.level
        if self.level == 100.0:
            raise Errors.fully_charged()
        if charging_left <= 0:
            minutes_spent = 0
            return minutes_spent
        minutes_spent = math.ceil(charging_left / self.settings.recharge_per_minute)
        return minutes_spent
    
    def charge(self, minutes):
        self.level += self.settings.recharge_per_minute * minutes
        if self.level > 100:
            self.level = 100

    def drain(self, minutes, mode):
        if mode == 'usage':
            self.level -= self.settings.drain_per_minute * minutes * self.settings.drain_factor_usage_mode
        elif mode == 'sleep':
            self.level -= self.settings.drain_per_minute * minutes * self.settings.drain_factor_sleep_mode
        elif mode == 'maintenance':
            self.level -= self.settings.drain_per_minute * minutes * self.settings.drain_factor_maintenance_mode
        if self.level < 0:
            self.level = 0
        else:
            raise Errors.invalid_mode()

    def is_low(self):
        return self.level < self.settings.minimum_battery_level_for_usage