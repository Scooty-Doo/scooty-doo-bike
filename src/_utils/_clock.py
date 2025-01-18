"""
Utility module for time-related tasks.
"""

import asyncio
from datetime import datetime, timezone

class Clock:
    """Class handling time-related tasks."""

    @staticmethod
    def now():
        """Return the current time in ISO format."""
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    async def sleep(seconds):
        """Sleep for a given number of seconds."""
        if not isinstance(seconds, (int, float)):
            raise TypeError("Seconds must be a number.")
        if seconds < 0:
            raise ValueError("Seconds cannot be negative.")
        await asyncio.sleep(seconds)

    @staticmethod
    def get_duration_in_minutes(distance_in_km, speed_in_kmh):
        """Return the duration in minutes for a given distance and speed"""
        return (distance_in_km / speed_in_kmh) * 60

    @staticmethod
    def convert_seconds_to_minutes(seconds):
        """Convert seconds to minutes."""
        return seconds / 60

    @staticmethod
    def get_leg_duration_in_seconds(total_duration_in_minutes, total_reports):
        """Return the duration of a leg in seconds."""
        return (total_duration_in_minutes / total_reports) * 60

# python -m src._utils._clock
# 2024-12-21T10:11:25.583095+00:00
