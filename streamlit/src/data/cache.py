from typing import Dict, Any
from datetime import datetime, timedelta
import json
import os

class DataCache:
    def __init__(self, cache_duration: int = 24):
        """
        Initialize cache with duration in hours
        """
        self.cache_duration = timedelta(hours=cache_duration)
        self.cache: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Dict[str, Any]:
        """Get data from cache if not expired"""
        if key in self.cache:
            data = self.cache[key]
            if datetime.now() - data['timestamp'] < self.cache_duration:
                return data['content']
        return None

    def set(self, key: str, content: Dict[str, Any]):
        """Set data in cache with timestamp"""
        self.cache[key] = {
            'content': content,
            'timestamp': datetime.now()
        }

    def is_valid(self, key: str) -> bool:
        """Check if cache entry is valid"""
        if key in self.cache:
            return datetime.now() - self.cache[key]['timestamp'] < self.cache_duration
        return False

    def clear(self):
        """Clear all cached data"""
        self.cache.clear()