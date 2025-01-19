# pylint: disable=too-few-public-methods
"""
This module handles the initialization of the bike hivemind.
"""

import httpx
from .._utils._settings import Settings

def _url(url, endpoint):
    """Concatenates the url and endpoint."""
    return f'{url.rstrip("/")}/{endpoint.lstrip("/")}'

class Initialize:
    """Class handling the initialization of the bike hivemind."""

    def __init__(self, token: str):
        self.endpoints = Settings.Endpoints()
        self.url = self.endpoints.backend_url
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }
        self.bikes = None # self._bikes().get('data', [])

    async def load_bikes(self):
        """Loads bikes from the backend."""
        if self.bikes is None:
            url = _url(self.url, self.endpoints.Bikes.get_all())
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(
                        url,
                        params={"limit": Settings.Endpoints.bike_limit},
                        headers=self.headers, timeout=20.0
                        )
                    response.raise_for_status()
                    self.bikes = response.json().get('data', [])
                    print(f'Bikes loaded. First five bikes: {self.bikes[0:5]}')
                except httpx.RequestError as e:
                    raise httpx.RequestError(f"Failed to request bikes: {e}") from e
        else:
            print(f'Bikes already loaded. First five bikes: {self.bikes[0:5]}')

    async def bike_ids(self):
        """Returns bike ids in a serialized format."""
        await self.load_bikes()
        return Serialize.bike_ids(Extract.Bike.ids(self.bikes))

    async def bike_positions(self):
        """Returns bike positions in a serialized format."""
        await self.load_bikes()
        return Serialize.positions(Extract.Bike.positions(self.bikes))

class Extract:
    """Class handling the extraction of data from the bikes."""
    class Bike:
        """Class handling the extraction of bike data."""
        @staticmethod
        def ids(bikes):
            """Extracts the bike ids."""
            return [bike['id'] for bike in bikes]

        @staticmethod
        def positions(bikes):
            """Extracts the last position e.g. "POINT(13.06782 55.577859)" and converts to tuple."""
            def _point_to_tuple(point):
                """Converts a point string to a tuple."""
                point = point.replace("POINT(", "").replace(")", "")
                return tuple(map(float, point.split()))
            return [_point_to_tuple(bike['attributes']['last_position']) for bike in bikes]

class Serialize:
    """Class handling the serialization of data."""
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
