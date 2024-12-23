import requests
import json
from typing import Union, List, Dict
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
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to request update: {e}")
    
    def zone_types(self):
        url = _url(self.url, self.endpoints.Zones.get_types)
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to request zone types: {e}")


class Logs():
    def __init__(self, url, headers):
        self.endpoints = Settings.Endpoints()
        self.url = url
        self.headers = headers

    def send(self, log: Union[Dict, List[Dict]]):
        url = _url(self.url, self.endpoints.Trips.start)
        if isinstance(log, dict):
            log = [log]
        try:
            for log in log:
                response = requests.post(url, headers=self.headers, data=json.dumps(log))
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to send logs: {e}")
        
    def update(self, logs: Union[Dict, List[Dict]]):
        url = _url(self.url, self.endpoints.Trips.update)
        if isinstance(logs, dict):
            logs = [logs]
        try:
            for log in logs:
                response = requests.patch(url, headers=self.headers, data=json.dumps(log))
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to update logs: {e}")


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
                response = requests.patch(url, headers=self.headers, data=json.dumps(report))
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to send reports: {e}")
