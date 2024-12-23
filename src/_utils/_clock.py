from datetime import datetime, timezone
import time

class Clock:

    @staticmethod
    def now():
        return datetime.now(timezone.utc).isoformat() # TODO: correct format?
    
    @staticmethod
    def sleep(seconds):
        if not isinstance(seconds, (int, float)):
            raise TypeError("Seconds must be a number.")
        if seconds < 0:
            raise ValueError("Seconds cannot be negative.")
        time.sleep(seconds)
    
    @staticmethod
    def get_duration_in_minutes(distance_in_km, speed_in_kmh):
        return (distance_in_km / speed_in_kmh) * 60
    
    @staticmethod
    def convert_seconds_to_minutes(seconds):
        return seconds / 60
    
    @staticmethod
    def get_leg_duration_in_seconds(total_duration_in_minutes, total_reports):
        return (total_duration_in_minutes / total_reports) * 60

# python -m src._utils._clock
# 2024-12-21T10:11:25.583095+00:00