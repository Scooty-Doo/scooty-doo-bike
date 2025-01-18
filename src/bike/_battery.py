"""
Module for the Battery class.
"""

import math
from .._utils._errors import Errors
from .._utils._settings import Settings

class Battery:
    """Class handling the battery of the bike."""

    def __init__(self, battery_level=100.0):
        self.level = battery_level
        self.settings = Settings.Battery()

    def get_charge_time(self, desired_level=100.0):
        """Get the time needed to charge the battery to a desired level."""
        charging_left = desired_level - self.level
        if self.level == 100.0:
            raise Errors.fully_charged()
        if charging_left <= 0:
            minutes_spent = 0
            return minutes_spent
        minutes_spent = math.ceil(charging_left / self.settings.recharge_per_minute)
        return minutes_spent

    def charge(self, minutes):
        """Charge the battery for a certain amount of time."""
        self.level += self.settings.recharge_per_minute * minutes
        self.level = min(self.level, 100)

    def drain(self, minutes, mode):
        """Drain the battery for a certain amount of time."""
        if mode == 'usage':
            self.level -= self.settings.drain_per_minute * \
                minutes * self.settings.drain_factor_usage_mode
        elif mode == 'sleep':
            self.level -= self.settings.drain_per_minute * \
                minutes * self.settings.drain_factor_sleep_mode
        elif mode == 'maintenance':
            self.level -= self.settings.drain_per_minute \
                * minutes * self.settings.drain_factor_maintenance_mode
        else:
            raise Errors.invalid_mode()
        self.level = max(self.level, 0)

    def is_low(self):
        """Check if the battery level is low."""
        return self.level < self.settings.minimum_battery_level_for_usage
