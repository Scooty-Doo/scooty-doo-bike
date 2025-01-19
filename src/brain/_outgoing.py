# pylint: disable=too-few-public-methods, too-many-instance-attributes
"""
This module handles outgoing communication to the backend.
"""

import json
from typing import Union, List, Dict
import httpx
from .._utils._settings import Settings

def _url(url, endpoint):
    """Concatenates the url and endpoint."""
    return f'{url.rstrip("/")}/{endpoint.lstrip("/")}'

class Outgoing:
    """Class handling outgoing communication to the backend."""
    def __init__(self, token: str, bike_id: int):
        self.endpoints = Settings.Endpoints()
        self.url = self.endpoints.backend_url
        self.token = token
        self.bike_id = bike_id
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }
        self.logs = Logs(self.url, self.headers)
        self.reports = Reports(self.url, self.headers, self.bike_id)
        self.request = Request(self.url, self.headers)

class Request():
    """Class handling requests to the backend."""
    def __init__(self, url, headers):
        self.endpoints = Settings.Endpoints()
        self.url = url
        self.headers = headers

    async def zones(self):
        """Requests all zones from the backend."""
        url = _url(self.url, self.endpoints.Zones.get_all)
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, timeout=20.0)
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                print(f"Failed to get zones {e}")

    async def zone_types(self):
        """Requests all zone types from the backend."""
        url = _url(self.url, self.endpoints.Zones.get_types)
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, timeout=20.0)
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                print(f"Failed to get zone types. {e}")

class Logs():
    """Class handling logs."""
    def __init__(self, url, headers):
        self.endpoints = Settings.Endpoints()
        self.url = url
        self.headers = headers

    async def send(self, logs: Union[Dict, List[Dict]]):
        """Sends logs to the backend."""
        url = _url(self.url, self.endpoints.Trips.start)
        if isinstance(logs, dict):
            logs = [logs]
        async with httpx.AsyncClient() as client:
            try:
                for log in logs:
                    response = await client.post(
                        url, headers=self.headers,
                        data=json.dumps(log), timeout=20.0)
                    response.raise_for_status()
            except httpx.RequestError as e:
                print(f"Failed to send log. {e}")

    async def update(self, logs: Union[Dict, List[Dict]]):
        """Updates logs in the backend."""
        url = _url(self.url, self.endpoints.Trips.update)
        if isinstance(logs, dict):
            logs = [logs]
        async with httpx.AsyncClient() as client:
            try:
                for log in logs:
                    response = await client.patch(
                        url, headers=self.headers,
                        data=json.dumps(log), timeout=20.0)
                    response.raise_for_status()
            except httpx.RequestError as e:
                print(f"Failed to send log. {e}")

class Reports():
    """Class handling reports."""
    def __init__(self, url, headers, bike_id):
        self.endpoints = Settings.Endpoints()
        self.url = url
        self.headers = headers
        self.bike_id = bike_id

    async def send(self, reports: Union[Dict, List[Dict]]):
        """Sends reports to the backend."""
        url = _url(self.url, self.endpoints.Bikes.update(self.bike_id))
        if isinstance(reports, dict):
            reports = [reports]
        async with httpx.AsyncClient() as client:
            try:
                for report in reports:
                    response = await client.patch(
                        url, headers=self.headers,
                        data=json.dumps(report), timeout=20.0)
                    response.raise_for_status()
            except httpx.RequestError as e:
                print(f"Failed to send report. {e}")
