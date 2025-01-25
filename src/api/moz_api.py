from typing import Dict, Any
import aiohttp
import asyncio
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

class MozClient:
    def __init__(self, api_token: str, rate_limiter):
        """
        Initialize MozClient with API token for authentication.
        :param api_token: API token provided for Moz API access.
        :param rate_limiter: A rate limiter instance to control API calls.
        """
        self.api_token = api_token
        self.headers = {
            'x-moz-token': self.api_token,
            'Content-Type': 'application/json'
        }
        self.base_url = "https://api.moz.com/jsonrpc"
        self.rate_limiter = rate_limiter

    async def get_domain_metrics(self, domain: str) -> Dict[str, Any]:
        """
        Fetch domain metrics from Moz API.
        :param domain: Domain to fetch metrics for.
        :return: A dictionary containing domain metrics or an error message.
        """
        await self.rate_limiter.wait_if_needed('moz')

        payload = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),  # Unique request ID
            "method": "data.site.metrics.fetch",
            "params": {
                "data": {
                    "site_query": {
                        "query": domain,
                        "scope": "domain"
                    }
                }
            }
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload
                ) as response:
                    if response.status != 200:
                        return {'error': f"API returned status {response.status}"}
                    data = await response.json()
                    return self._process_domain_metrics(data.get("result", {}))
            except Exception as e:
                return {'error': str(e)}

    def _process_domain_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process and structure the Moz API response data.
        :param data: Raw response data from Moz API.
        :return: A dictionary with structured domain metrics.
        """
        site_metrics = data.get("site_metrics", {})
        return {
            'domain_authority': site_metrics.get('domain_authority', 0),
            'page_authority': site_metrics.get('page_authority', 0),
            'linking_domains': site_metrics.get('root_domains_to_root_domain', 0),
            'total_links': site_metrics.get('pages_to_root_domain', 0),
            'spam_score': site_metrics.get('spam_score', 0),
            'last_crawled': site_metrics.get('last_crawled', 'N/A'),
        }


# Example usage:
if __name__ == "__main__":
    class MockRateLimiter:
        async def wait_if_needed(self, api_name):
            await asyncio.sleep(0.1)  # Simulate rate limiting

    # Replace with your Moz API token
    API_TOKEN = os.getenv("MOZ_TOKEN")

    moz_client = MozClient(API_TOKEN, MockRateLimiter())

    async def main():
        domain = "https://moz.com/blog"
        print("Fetching domain metrics...")
        domain_metrics = await moz_client.get_domain_metrics(domain)
        print(domain_metrics)

    asyncio.run(main())
