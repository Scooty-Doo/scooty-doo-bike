"""
Module centralizing all settings for the application.
"""

import os

class Settings:
    """Class handling all settings for the application."""

    class Position:
        """Class handling all settings for the position of the bike."""
        default_longitude = float(0.0)
        default_latitude = float(0.0)

    class Speed:
        """Class handling all settings for the speed of the bike."""
        default_speed_limit = int(os.getenv("DEFAULT_SPEED", "20"))

    class Battery:
        """Class handling all settings for the battery of the bike."""
        drain_per_minute = 0.05
        drain_factor_usage_mode = 1.0
        drain_factor_sleep_mode = 0.5
        drain_factor_maintenance_mode = 0.0
        recharge_per_minute = 5.0
        minimum_battery_level_for_usage = 20.0

    class Endpoints:
        """Class handling all settings for the endpoints of the application."""
        backend_url = os.getenv("BACKEND_URL")
        bike_id = os.getenv("BIKE_ID")
        bike_limit = int(os.getenv("BIKE_LIMIT", "9999"))

        # NOTE: Endpoints need to get the values through parameters
        # (convert attribute to method) or environment (if BIKE_ID).
        # Change this if you need other endpoints.

        class Bikes:
            """Class handling all settings for the bike endpoints."""
            endpoint = 'v1/bikes/'
            @staticmethod
            def get_all():
                """Get all bikes."""
                return f'{Settings.Endpoints.Bikes.endpoint}'
            @staticmethod
            def get(bike_id: int):
                """Get a bike."""
                return f'{Settings.Endpoints.Bikes.endpoint}{bike_id}'
            @staticmethod
            def add():
                """Add a bike."""
                return f'{Settings.Endpoints.Bikes.endpoint}'
            @staticmethod
            def update(bike_id: int):
                """Update a bike."""
                return f'{Settings.Endpoints.Bikes.endpoint}{bike_id}'
            @staticmethod
            def remove(bike_id: int):
                """Remove a bike."""
                return f'{Settings.Endpoints.Bikes.endpoint}{bike_id}'

        class Trips:
            """Class handling all settings for the trip endpoints."""
            endpoint = 'v1/trips/'
            get_all = f'{endpoint}'
            start = f'{endpoint}'
            get = f'{endpoint}{{id}}'
            update = f'{endpoint}{{id}}'
            remove = f'{endpoint}{{id}}'
            get_for_bike = f'{endpoint}bike/{{id}}'
            get_trip_for_bike = f'{endpoint}bike/{{id}}/trip/{{trip_id}}'
            get_user_history = f'{endpoint}user/{{id}}'

        class Zones:
            """Class handling all settings for the zone endpoints."""
            endpoint = 'v1/zones/'
            get_all = f'{endpoint}'
            create = f'{endpoint}'
            get = f'{endpoint}{{id}}'
            update = f'{endpoint}{{id}}'
            remove = f'{endpoint}{{id}}'
            get_parking = f'{endpoint}parking'
            get_types = f'{endpoint}types'

        class Users:
            """Class handling all settings for the user endpoints."""
            endpoint = 'v1/users/'
            get_all = f'{endpoint}'
            create = f'{endpoint}'
            get = f'{endpoint}{{id}}'

    class Report:
        """Class handling all settings for the regular reports."""
        interval = 10
        interval_sleep = 300
        interval_maintenance = 600
        interval_usage = 10
