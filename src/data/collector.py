from typing import Dict, Any
from ..api import MozClient
from ..scraper import SEOScraper
import asyncio


class DataCollector:
    def __init__(self, moz_client: MozClient, cache):
        """
        Initialize the DataCollector with Moz API client and scraper.
        :param moz_client: Instance of MozClient.
        :param cache: Cache for storing collected data.
        """
        self.moz_client = moz_client
        self.scraper = SEOScraper()
        self.cache = cache

    async def collect_all_data(self, url: str) -> Dict[str, Any]:
        """
        Collect all data for a given URL.
        :param url: The URL to collect data for.
        :return: Aggregated data from Moz API and scraper.
        """
        # Check cache first
        cache_key = f"data_{url}"
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data

        # Collect data from all sources
        try:
            # Run collectors concurrently
            moz_task = self.collect_moz_data(url)
            scraper_task = self.collect_scraped_data(url)

            moz_data, scraped_data = await asyncio.gather(
                moz_task, scraper_task
            )

            collected_data = {
                'moz_data': moz_data,
                'scraped_data': scraped_data
            }

            # Cache the results
            self.cache.set(cache_key, collected_data)
            return collected_data

        except Exception as e:
            return {'error': str(e)}

    async def collect_moz_data(self, url: str) -> Dict[str, Any]:
        """
        Collect Moz API data.
        :param url: The URL to collect Moz metrics for.
        :return: Moz metrics and backlink data.
        """
        try:
            metrics = await self.moz_client.get_domain_metrics(url)
            backlinks = await self.moz_client.get_backlinks(url)
            return {
                'metrics': metrics,
                'backlinks': backlinks
            }
        except Exception as e:
            return {'error': str(e)}

    async def collect_scraped_data(self, url: str) -> Dict[str, Any]:
        """
        Collect scraped data.
        :param url: The URL to scrape.
        :return: Scraped page data.
        """
        try:
            return await self.scraper.scrape_page(url)
        except Exception as e:
            return {'error': str(e)}
