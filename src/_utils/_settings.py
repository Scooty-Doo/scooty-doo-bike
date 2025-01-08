import os

class Settings:

    class Position:
        default_longitude = float(0.0)
        default_latitude = float(0.0)

    class Speed:
        default_speed_limit = 100

    class Battery:
        drain_per_minute = 0.05
        drain_factor_usage_mode = 1.0
        drain_factor_sleep_mode = 0.5
        drain_factor_maintenance_mode = 0.0
        recharge_per_minute = 5.0
        minimum_battery_level_for_usage = 20.0

    class Endpoints:
        backend_url = os.getenv("BACKEND_URL")
        bike_id = os.getenv("BIKE_ID")

        # TODO: Endpoints need to get the values through parameters
        # (convert attribute to method) or environment (if BIKE_ID).

        class Bikes:
            endpoint = 'v1/bikes/'
            @staticmethod
            def get_all():
                return f'{Settings.Endpoints.Bikes.endpoint}'
            @staticmethod
            def get(bike_id: int):
                return f'{Settings.Endpoints.Bikes.endpoint}{bike_id}'
            @staticmethod
            def add():
                return f'{Settings.Endpoints.Bikes.endpoint}'
            @staticmethod
            def update(bike_id: int):
                return f'{Settings.Endpoints.Bikes.endpoint}{bike_id}'
            @staticmethod
            def remove(bike_id: int):
                return f'{Settings.Endpoints.Bikes.endpoint}{bike_id}'

        class Trips:
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
            endpoint = 'v1/zones/'
            get_all = f'{endpoint}'
            create = f'{endpoint}'
            get = f'{endpoint}{{id}}'
            update = f'{endpoint}{{id}}'
            remove = f'{endpoint}{{id}}'
            get_parking = f'{endpoint}parking'
            get_types = f'{endpoint}types'

        class Users:
            endpoint = 'v1/users/'
            get_all = f'{endpoint}'
            create = f'{endpoint}'
            get = f'{endpoint}{{id}}'

    class Report:
        interval = 5
        interval_sleep = 60
        interval_maintenance = 60
        interval_usage = 5
