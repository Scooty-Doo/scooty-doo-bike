import json
from typing import Union, List, Dict
import requests
from .._utils._settings import Settings

def _url(url, endpoint):
    return f'{url}/{endpoint}'

class Outgoing:
    def __init__(self, token):
        self.endpoints = Settings.Endpoints()
        self.url = self.endpoints.backend_url
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }
        self.logs = Logs(self.url, self.headers)
        self.reports = Reports(self.url, self.headers)
        self.request = Request(self.url, self.headers)

class Request():
    def __init__(self, url, headers):
        self.endpoints = Settings.Endpoints()
        self.url = url
        self.headers = headers

    def zones(self):
        url = _url(self.url, self.endpoints.Zones.get_all)
        try:
            response = requests.get(url, headers=self.headers, timeout=(5, 10))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Failed to request zones: {e}") from e

    def zone_types(self):
        url = _url(self.url, self.endpoints.Zones.get_types)
        try:
            response = requests.get(url, headers=self.headers, timeout=(5, 10))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Failed to request zone types: {e}") from e

class Logs():
    def __init__(self, url, headers):
        self.endpoints = Settings.Endpoints()
        self.url = url
        self.headers = headers

    def send(self, logs: Union[Dict, List[Dict]]):
        url = _url(self.url, self.endpoints.Trips.start)
        if isinstance(logs, dict):
            logs = [logs]
        try:
            for log in logs:
                response = requests.post(
                    url, headers=self.headers,
                    data=json.dumps(log), timeout=(5, 10))
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Failed to send logs: {e}") from e

    def update(self, logs: Union[Dict, List[Dict]]):
        url = _url(self.url, self.endpoints.Trips.update)
        if isinstance(logs, dict):
            logs = [logs]
        try:
            for log in logs:
                response = requests.patch(
                    url, headers=self.headers,
                    data=json.dumps(log), timeout=(5, 10))
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Failed to update logs: {e}") from e

class Reports():
    def __init__(self, url, headers):
        self.endpoints = Settings.Endpoints()
        self.url = url
        self.headers = headers

    def send(self, reports: Union[Dict, List[Dict]]):
        url = _url(self.url, self.endpoints.Bikes.update)
        if isinstance(reports, dict):
            reports = [reports]
        try:
            for report in reports:
                response = requests.patch(
                    url, headers=self.headers,
                    data=json.dumps(report), timeout=(5, 10))
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Failed to send reports: {e}") from e
