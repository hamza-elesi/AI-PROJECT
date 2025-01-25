import asyncio
import time
from typing import Dict
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self):
        self.limits = {
            'moz': {'calls': 25, 'period': 'day'},     # Free tier limits
            'gsc': {'calls': 25000, 'period': 'day'}   # GSC daily quota
        }
        self.calls: Dict[str, list] = {
            'moz': [],
            'gsc': []
        }

    def can_make_request(self, api_name: str) -> bool:
        now = datetime.now()
        # Clean old calls
        self.calls[api_name] = [
            call_time for call_time in self.calls[api_name]
            if now - call_time < timedelta(days=1)
        ]
        
        return len(self.calls[api_name]) < self.limits[api_name]['calls']

    def log_request(self, api_name: str):
        self.calls[api_name].append(datetime.now())

    async def wait_if_needed(self, api_name: str):
        while not self.can_make_request(api_name):
            await asyncio.sleep(1)
        self.log_request(api_name)