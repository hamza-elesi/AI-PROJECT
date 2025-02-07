from typing import Dict, Any
from ..scraper.web_scraper import SEOScraper
import asyncio


class DataCollector:
    def __init__(self, moz_client, scraper, cache):
        """
        Initialize the DataCollector with Moz API client and scraper.
        :param moz_client: Instance of MozClient.
        :param scraper: Instance of SEOScraper.
        :param cache: Cache for storing collected data.
        """
        self.moz_client = moz_client
        self.scraper = scraper
        self.cache = cache

    async def collect_all_data(self, url: str) -> Dict[str, Any]:
        """
        Collect all data for a given URL.
        :param url: The URL to collect data for.
        :return: Aggregated data from Moz API and scraper.
        """
        # ✅ Check if data exists in cache first
        cache_key = f"data_{url}"
        cached_data = self.cache.get(cache_key)
        if cached_data:
            print(f"✅ Using Cached Data for {url}")
            return cached_data

        try:
            print(f"🔍 Collecting new SEO data for {url}...")

            # ✅ Run Moz API and Web Scraping concurrently
            moz_task = self.collect_moz_data(url)
            scraper_task = self.collect_scraped_data(url)

            moz_data, scraped_data = await asyncio.gather(moz_task, scraper_task)

            # ✅ Ensure all data is collected properly
            if not moz_data:
                print("⚠️ Warning: Moz API returned empty results.")
                moz_data = {}

            if not scraped_data:
                print("⚠️ Warning: Scraped data is empty.")
                scraped_data = {}

            collected_data = {
                "overview": self._combine_overview_data(moz_data, scraped_data),
                "moz_data": moz_data,
                "scraped_data": scraped_data,
            }

            # ✅ Store results in cache for fast retrieval
            self.cache.set(cache_key, collected_data)
            print("✅ SEO Data Collection Complete")
            return collected_data

        except Exception as e:
            print(f"❌ Data Collection Error: {e}")
            return {"error": str(e)}

    async def collect_moz_data(self, url: str) -> Dict[str, Any]:
        """
        Collect Moz API data.
        :param url: The URL to collect Moz metrics for.
        :return: Moz metrics and backlink data.
        """
        try:
            print(f"📊 Fetching Moz Metrics for {url}...")
            metrics = await self.moz_client.get_domain_metrics(url)

            if not metrics:
                print("⚠️ Moz Metrics Data is Empty")
                return {}

            return {"metrics": metrics}

        except Exception as e:
            print(f"❌ Moz API Error: {e}")
            return {"error": str(e)}

    async def collect_scraped_data(self, url: str) -> Dict[str, Any]:
        """
        Collect scraped data.
        :param url: The URL to scrape.
        :return: Scraped page data.
        """
        try:
            print(f"🌍 Scraping Page Data for {url}...")
            scraped_data = await self.scraper.scrape_page(url)

            if not scraped_data:
                print("⚠️ Scraped Data is Empty")
                return {}

            return scraped_data

        except Exception as e:
            print(f"❌ Scraper Error: {e}")
            return {"error": str(e)}

    def _combine_overview_data(self, moz_data: Dict, scraped_data: Dict) -> Dict:
        """
        Combines overview data from Moz API and scraped content.
        """
        return {
            "domain_authority": moz_data.get("metrics", {}).get("domain_authority", 0),
            "page_authority": moz_data.get("metrics", {}).get("page_authority", 0),
            "meta_tags": scraped_data.get("meta_tags", {}),
            "total_links": moz_data.get("metrics", {}).get("total_links", 0),
            "backlink_profile": moz_data.get("metrics", {}).get("linking_domains", 0),
            "content_quality": scraped_data.get("content", {}).get("word_count", 0),
        }