from datetime import datetime, timezone

class Clock:

    @staticmethod
    def now():
        return datetime.now(timezone.utc).isoformat() # TODO: correct format?