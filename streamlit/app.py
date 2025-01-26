import asyncio
import streamlit as st
from components.metrics import MetricsDisplay
from components.report import ReportDisplay
from src.data.collector import DataCollector
from src.reports.generator import ReportGenerator
from src.api.moz_api import MozClient
from src.scraper.web_scraper import SEOScraper
from src.data.cache import DataCache
from src.api.rate_limiter import RateLimiter
import os
from dotenv import load_dotenv

load_dotenv()


class SEOApp:
    def __init__(self, data_collector, report_generator):
        self.data_collector = data_collector
        self.report_generator = report_generator

    def run(self):
        st.title("SEO Analysis Tool")
        url = st.text_input("Enter the website URL", placeholder="https://example.com")

        if url:
            with st.spinner("Analyzing website..."):
                try:
                    collected_data = asyncio.run(self.data_collector.collect_all_data(url))
                    self._display_results(collected_data)
                except Exception as e:
                    st.error(f"Error analyzing website: {str(e)}")

    def _display_results(self, data):
        """Display analysis results."""
        MetricsDisplay.show_overview(data.get("overview", {}))
        ReportDisplay.show_technical_analysis(data.get("scraped_data", {}))
        ReportDisplay.show_backlink_analysis(data.get("moz_data", {}).get("metrics", {}))


if __name__ == "__main__":
    rate_limiter = RateLimiter()
    moz_client = MozClient(api_token=os.getenv("MOZ_TOKEN"), rate_limiter=rate_limiter)
    scraper = SEOScraper()
    cache = DataCache()
    data_collector = DataCollector(moz_client, scraper, cache)
    report_generator = ReportGenerator()

    app = SEOApp(data_collector, report_generator)
    app.run()
