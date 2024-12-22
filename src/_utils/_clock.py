from datetime import datetime, timezone
from time import sleep

class Clock:

    @staticmethod
    def now():
        return datetime.now(timezone.utc).isoformat() # TODO: correct format?
    
    @staticmethod
    def sleep(seconds):
        sleep(seconds)

if __name__ == "__main__":
    print(Clock.now())

# python -m src._utils._clock
# 2024-12-21T10:11:25.583095+00:00