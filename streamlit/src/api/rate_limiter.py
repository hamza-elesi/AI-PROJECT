import asyncio
import time
from typing import Dict, List
from datetime import datetime, timedelta


class RateLimiter:
    def __init__(self):
        """
        Initializes the RateLimiter with API rate limits and call tracking.
        """
        self.limits = {
            'moz': {'calls': 25, 'period': 'day'},  # Free tier limits for Moz
        }
        self.calls: Dict[str, List[datetime]] = {
            api_name: [] for api_name in self.limits
        }

    def _get_period_seconds(self, period: str) -> int:
        """
        Converts a period string to seconds.
        :param period: The period string ('day', 'hour', 'minute').
        :return: The equivalent number of seconds.
        """
        if period == 'day':
            return 86400  # 24 hours in seconds
        elif period == 'hour':
            return 3600  # 1 hour in seconds
        elif period == 'minute':
            return 60  # 1 minute in seconds
        else:
            raise ValueError(f"Unknown period: {period}")

    def can_make_request(self, api_name: str) -> bool:
        """
        Checks if a request can be made for a given API.
        :param api_name: The name of the API (e.g., 'moz').
        :return: True if a request can be made, False otherwise.
        """
        now = datetime.now()
        period_seconds = self._get_period_seconds(self.limits[api_name]['period'])
        # Remove outdated calls from the log
        self.calls[api_name] = [
            call_time for call_time in self.calls[api_name]
            if (now - call_time).total_seconds() < period_seconds
        ]
        # Check if the number of calls is within the limit
        return len(self.calls[api_name]) < self.limits[api_name]['calls']

    def log_request(self, api_name: str):
        """
        Logs a request for a given API.
        :param api_name: The name of the API (e.g., 'moz').
        """
        self.calls[api_name].append(datetime.now())

    async def wait_if_needed(self, api_name: str):
        """
        Waits if the request limit for a given API has been reached.
        :param api_name: The name of the API (e.g., 'moz').
        """
        while not self.can_make_request(api_name):
            await asyncio.sleep(1)
        self.log_request(api_name)
