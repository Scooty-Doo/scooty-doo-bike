from .._utils._errors import Errors

class Mode:
    def __init__(self, mode='maintenance'):
        self.current = mode
        self.modes = ['sleep', 'usage', 'maintenance']
        if mode not in self.modes:
            raise Errors.invalid_mode()

    def usage(self):
        self.current = 'usage'

    def maintenance(self):
        self.current = 'maintenance'
    
    def sleep(self):
        self.current = 'sleep'

    def is_usage(self):
        return True if self.current == 'usage' else False
    
    def is_maintenance(self):
        return True if self.current == 'maintenance' else False
    
    def is_sleep(self):
        return True if self.current == 'sleep' else False

    def is_unlocked(self):
        return True if self.current == 'usage' else False
    
    def is_locked(self):
        return True if self.current in ['maintenance', 'sleep'] else False