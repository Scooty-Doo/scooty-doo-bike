import os

class Settings:
    
    class Position:
        default_longitude = 0.0
        default_latitude = 0.0

    class Speed:
        max_speed = 20

    class Battery:
        drain_per_minute = 0.05
        drain_factor_usage_mode = 1.0
        drain_factor_sleep_mode = 0.5
        drain_factor_maintenance_mode = 0.0
        recharge_per_minute = 5.0
        minimum_battery_level_for_usage = 20.0

    class Endpoints:
        backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")

        class Bikes:
            endpoint = 'v1/bikes'
            get_all = f'{endpoint}'
            get = f'{endpoint}' + '/{bike_id}'
            add = f'{endpoint}'
            update = f'{endpoint}' + '/{bike_id}'
            remove = f'{endpoint}' + '/{bike_id}'
        
        class Trips:
            endpoint = 'v1/trips'
            get_all = f'{endpoint}'
            start = f'{endpoint}'
            get = f'{endpoint}/{{id}}'
            update = f'{endpoint}/{{id}}'
            remove = f'{endpoint}/{{id}}'
            get_for_bike = f'{endpoint}/bike/{{id}}'
            get_trip_for_bike = f'{endpoint}/bike/{{id}}/trip/{{trip_id}}'
            get_user_history = f'{endpoint}/user/{{id}}'

        class Zones:
            endpoint = 'v1/zones'
            get_all = f'{endpoint}'
            create = f'{endpoint}'
            get = f'{endpoint}/{{id}}'
            update = f'{endpoint}/{{id}}'
            remove = f'{endpoint}/{{id}}'
            get_parking = f'{endpoint}/parking'

        class Users:
            endpoint = 'v1/users'
            get_all = f'{endpoint}'
            create = f'{endpoint}'
            get = f'{endpoint}/{{id}}'

    class Report:
        report_interval = 5
