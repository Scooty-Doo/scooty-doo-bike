"""
Module for the Mode class.
"""

from .._utils._errors import Errors

class Mode:
    """Class handling the mode of the bike."""
    def __init__(self, mode='sleep'):
        self.current = mode
        self.modes = ['sleep', 'usage', 'maintenance']
        self.submodes = _Submodes()
        if mode not in self.modes:
            raise Errors.invalid_mode()

    def usage(self):
        """Set the mode to usage."""
        self.current = 'usage'

    def maintenance(self):
        """Set the mode to maintenance."""
        self.current = 'maintenance'

    def sleep(self):
        """Set the mode to sleep."""
        self.current = 'sleep'

    def is_usage(self):
        """Check if the mode is usage."""
        return self.current == 'usage'

    def is_maintenance(self):
        """Check if the mode is maintenance."""
        return self.current == 'maintenance'

    def is_sleep(self):
        """Check if the mode is sleep."""
        return self.current == 'sleep'

    def is_unlocked(self):
        """Check if the bike is unlocked."""
        return self.current == 'usage'

    def is_locked(self):
        """Check if the bike is locked."""
        return self.current in ['maintenance', 'sleep']

class _Submodes:
    """Class handling the submodes of the bike."""
    def __init__(self):
        self.usage = _Usage()

class _Usage:
    """Class handling the usage submodes of the bike."""
    def __init__(self):
        self.submodes = ['is_moving', 'is_charging']
        self.moving = False
        self.charging = False

    def is_moving(self):
        """Check if the bike is moving."""
        return self.moving

    def is_charging(self):
        """Check if the bike is charging."""
        return self.charging
