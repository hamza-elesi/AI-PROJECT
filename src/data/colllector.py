from typing import Dict, Any, Optional
from ..api import GSCClient, MozClient
from ..scraper import SEOScraper
import asyncio

class DataCollector:
    def __init__(self, gsc_client: GSCClient, moz_client: MozClient, cache):
        self.gsc_client = gsc_client
        self.moz_client = moz_client
        self.scraper = SEOScraper()
        self.cache = cache

    async def collect_all_data(self, url: str) -> Dict[str, Any]:
        """
        Collect all data for a given URL
        """
        # Check cache first
        cache_key = f"data_{url}"
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data

        # Collect data from all sources
        try:
            # Run all collectors concurrently
            gsc_task = self.collect_gsc_data(url)
            moz_task = self.collect_moz_data(url)
            scraper_task = self.collect_scraped_data(url)

            gsc_data, moz_data, scraped_data = await asyncio.gather(
                gsc_task, moz_task, scraper_task
            )

            collected_data = {
                'gsc_data': gsc_data,
                'moz_data': moz_data,
                'scraped_data': scraped_data
            }

            # Cache the results
            self.cache.set(cache_key, collected_data)
            return collected_data

        except Exception as e:
            return {'error': str(e)}

    async def collect_gsc_data(self, url: str) -> Dict[str, Any]:
        """Collect Google Search Console data"""
        try:
            analytics = await self.gsc_client.get_search_analytics(url)
            sitemaps = await self.gsc_client.get_sitemaps(url)
            return {
                'analytics': analytics,
                'sitemaps': sitemaps
            }
        except Exception as e:
            return {'error': str(e)}

    async def collect_moz_data(self, url: str) -> Dict[str, Any]:
        """Collect Moz API data"""
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
        """Collect scraped data"""
        try:
            return await self.scraper.scrape_page(url)
        except Exception as e:
            return {'error': str(e)}