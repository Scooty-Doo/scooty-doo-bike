import httpx
from .._utils._settings import Settings

def _url(url, endpoint):
    return f'{url.rstrip("/")}/{endpoint.lstrip("/")}'

class Initialize:
    def __init__(self, token: str):
        self.endpoints = Settings.Endpoints()
        self.url = self.endpoints.backend_url
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }
        self.bikes = self._bikes()
        print(f'Bikes look like this: {self.bikes}')

    def _bikes(self):
        url = _url(self.url, self.endpoints.Bikes.get_all())
        with httpx.Client() as client:
            try:
                response = client.get(url, headers=self.headers, timeout=10.0)
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise httpx.RequestError(f"Failed to request bikes: {e}") from e

    def bike_ids(self):
        bikes = self.bikes
        return Extract.Bike.ids(bikes)
    
    def bike_positions(self):
        bikes = self.bikes
        return Extract.Bike.positions(bikes)

class Extract:
    class Bike:
        @staticmethod
        def ids(bikes):
            return [bike['data']['id'] for bike in bikes]

        @staticmethod
        def positions(bikes):
            """Extracts the last position e.g. "POINT(13.06782 55.577859)" and converts to tuple."""
            def _point_to_tuple(point):
                point = point.replace("POINT(", "").replace(")", "")
                return tuple(map(float, point.split()))
            return [_point_to_tuple(bike['data']['attributes']['last_position']) for bike in bikes]

class Serialize:
    @staticmethod
    def positions(positions: list[tuple[float, float]]) -> list[str]:
        """
        Serializes positions from tuples to a a list of "longitude:latitude" strings.
        For storage in environment file.
        """
        return ','.join([f"{longitude}:{latitude}" for (longitude, latitude) in positions])

    @staticmethod
    def bike_ids(bike_ids: list[int]) -> str:
        """
        Serializes bike ids to a comma-separated string.
        For storage in environment file.
        """
        return ','.join(map(str, bike_ids))