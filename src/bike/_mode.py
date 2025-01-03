from .._utils._errors import Errors

class Mode:
    def __init__(self, mode='maintenance'):
        self.current = mode
        self.modes = ['sleep', 'usage', 'maintenance']
        self.submodes = _Submodes()
        if mode not in self.modes:
            raise Errors.invalid_mode()

    def usage(self):
        self.current = 'usage'

    def maintenance(self):
        self.current = 'maintenance'

    def sleep(self):
        self.current = 'sleep'

    def is_usage(self):
        return self.current == 'usage'

    def is_maintenance(self):
        return self.current == 'maintenance'

    def is_sleep(self):
        return self.current == 'sleep'

    def is_unlocked(self):
        return self.current == 'usage'

    def is_locked(self):
        return self.current in ['maintenance', 'sleep']

class _Submodes:
    def __init__(self):
        self.usage = _Usage()

class _Usage:
    def __init__(self):
        self.submodes = ['is_moving', 'is_charging']
        self.moving = False
        self.charging = False
    
    def is_moving(self):
        return self.is_moving

    def is_charging(self):
        return self.is_charging
