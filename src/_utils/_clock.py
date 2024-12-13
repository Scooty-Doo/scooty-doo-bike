from datetime import datetime, timezone
from time import sleep

class Clock:

    @staticmethod
    def now():
        return datetime.now(timezone.utc).isoformat() # TODO: correct format?
    
    @staticmethod
    def sleep(seconds):
        sleep(seconds)