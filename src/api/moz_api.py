from typing import Dict, Any, Optional
import aiohttp
import asyncio
from urllib.parse import quote_plus

# api/moz_api.py
class MozClient:
    def __init__(self, token: str, rate_limiter):
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

    async def get_domain_metrics(self, domain: str) -> Dict[str, Any]:
        """Get domain authority and metrics from Moz"""
        await self.rate_limiter.wait_if_needed('moz')
        
        url = f"{self.base_url}/urlmetrics"
        headers = {
            'Authorization': f'Basic {self.access_id}:{self.secret_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    headers=headers,
                    params={'url': quote_plus(domain)}
                ) as response:
                    data = await response.json()
                    return self._process_domain_metrics(data)
        except Exception as e:
            return {'error': str(e)}

    def _process_domain_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process and structure the Moz API response data"""
        return {
            'domain_authority': data.get('domain_authority', 0),
            'page_authority': data.get('page_authority', 0),
            'linking_domains': data.get('linking_domains', 0),
            'total_links': data.get('total_links', 0),
            'spam_score': data.get('spam_score', 0)
        }

    async def get_backlinks(self, domain: str, limit: int = 50) -> Dict[str, Any]:
        """Get backlink data from Moz"""
        await self.rate_limiter.wait_if_needed('moz')
        
        url = f"{self.base_url}/links"
        headers = {
            'Authorization': f'Basic {self.access_id}:{self.secret_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    headers=headers,
                    params={
                        'url': quote_plus(domain),
                        'limit': limit
                    }
                ) as response:
                    return await response.json()
        except Exception as e:
            return {'error': str(e)}