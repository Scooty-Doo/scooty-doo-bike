import json
from typing import Union, List, Dict
import httpx
from .._utils._settings import Settings

def _url(url, endpoint):
    return f'{url.rstrip("/")}/{endpoint.lstrip("/")}'

class Outgoing:
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
    def __init__(self, url, headers):
        self.endpoints = Settings.Endpoints()
        self.url = url
        self.headers = headers

    async def zones(self):
        url = _url(self.url, self.endpoints.Zones.get_all)
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, timeout=20.0)
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise httpx.RequestError(f"Failed to request zones: {e}") from e

    async def zone_types(self):
        url = _url(self.url, self.endpoints.Zones.get_types)
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, timeout=20.0)
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise httpx.RequestError(f"Failed to request zone types: {e}") from e

class Logs():
    def __init__(self, url, headers):
        self.endpoints = Settings.Endpoints()
        self.url = url
        self.headers = headers

    async def send(self, logs: Union[Dict, List[Dict]]):
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
                raise httpx.RequestError(f"Failed to send logs: {e}") from e

    async def update(self, logs: Union[Dict, List[Dict]]):
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
                raise httpx.RequestError(f"Failed to update logs: {e}") from e

class Reports():
    def __init__(self, url, headers, bike_id):
        self.endpoints = Settings.Endpoints()
        self.url = url
        self.headers = headers
        self.bike_id = bike_id

    async def send(self, reports: Union[Dict, List[Dict]]):
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
                raise httpx.RequestError(f"Failed to send reports: {e}") from e
