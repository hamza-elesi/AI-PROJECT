import traceback
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
        try:
            print(f"🔍 Collecting new SEO data for {url}...")

            # Run Moz API and Web Scraping concurrently
            moz_data, scraped_data = await asyncio.gather(
                self.collect_moz_data(url),
                self.collect_scraped_data(url)
            )


            # collector.py (inside collect_all_data)
            collected_data = {
                "overview": self._combine_overview_data(moz_data, scraped_data),
                "scraped_data": self._extract_technical_data(scraped_data),  # ✅ Direct scraped data
                "content_data": self._extract_content_data(scraped_data),
                "backlink_data": self._extract_backlink_data(moz_data),
                "raw_data": {
                    "moz_data": moz_data,
                    "scraped_data": scraped_data
                }
            }

            return collected_data

        except Exception as e:
            print(f"❌ Data Collection Error: {e}")
            return {"error": str(e)}
    # collector.py
    def _extract_technical_data(self, scraped_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract technical SEO metrics from scraped data"""
        if 'error' in scraped_data:
            return {
                'status': 'error',
                'message': scraped_data['error']
            }
        return scraped_data  # ✅ Return scraped data directly

    def _extract_content_data(self, scraped_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract content metrics from scraped data"""
        if 'error' in scraped_data:
            return {
                'status': 'error',
                'message': scraped_data['error']
            }
        
        return {
            'status': 'success',
            'metrics': {
                'content': scraped_data.get('content', {}),
                'images': scraped_data.get('images', {}),
                'links': scraped_data.get('links', {})
            }
        }

    def _extract_backlink_data(self, moz_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract backlink metrics from Moz data"""
        metrics = moz_data.get('metrics', {})
        return {
            'status': 'success',
            'metrics': {
                'domain_authority': metrics.get('domain_authority', 0),
                'page_authority': metrics.get('page_authority', 0),
                'linking_domains': metrics.get('linking_domains', 0),
                'total_links': metrics.get('total_links', 0),
                'spam_score': metrics.get('spam_score', 0)
            }
        }
    async def collect_moz_data(self, url: str) -> Dict[str, Any]:
        try:
            print(f"📊 Fetching Moz Metrics for {url}...")
            
            # Add debug logging
            print(f"🔍 Moz Client: {self.moz_client}")
            
            metrics = await self.moz_client.get_domain_metrics(url)
            
            # Add more detailed logging
            print(f"🔍 Moz API Response: {metrics}")
            
            if not metrics:
                print("⚠️ Moz Metrics Data is Empty - Possible Reasons:")
                print("1. Invalid API credentials")
                print("2. URL not in Moz's index")
                print("3. API rate limit exceeded")
                return {}
                
            return {"metrics": metrics}
        except Exception as e:
            print(f"❌ Moz API Error: {e}")
            print(f"❌ Stack Trace: {traceback.format_exc()}")
            return {"error": str(e)}

    # async def collect_moz_data(self, url: str) -> Dict[str, Any]:
    #     """
    #     Collect Moz API data.
    #     :param url: The URL to collect Moz metrics for.
    #     :return: Moz metrics and backlink data.
    #     """
    #     try:
    #         print(f"📊 Fetching Moz Metrics for {url}...")
    #         metrics = await self.moz_client.get_domain_metrics(url)

    #         if not metrics:
    #             print("⚠️ Moz Metrics Data is Empty")
    #             return {}

    #         return {"metrics": metrics}

    #     except Exception as e:
    #         print(f"❌ Moz API Error: {e}")
    #         return {"error": str(e)}

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