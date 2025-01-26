import streamlit as st
from data.collector import DataCollector
from reports.generator import ReportGenerator
from .config import Config
from .components.metrics import MetricsDisplay
from .components.report import ReportDisplay
from typing import Dict, Any
import os
from dotenv import load_dotenv
import asyncio
load_dotenv()

class SEOApp:
    def __init__(self, data_collector: DataCollector, report_generator: ReportGenerator):
        """
        Initialize the SEO app with its dependencies.
        :param data_collector: Instance of DataCollector for data gathering.
        :param report_generator: Instance of ReportGenerator for creating reports.
        """
        self.data_collector = data_collector
        self.report_generator = report_generator
        Config.setup_page()

    def run(self):
        """Main app execution."""
        st.title("SEO Analysis Tool")
        
        # URL Input
        url = st.text_input(
            "Enter the website URL",
            placeholder="https://example.com"
        )
        
        if url:
            with st.spinner("Analyzing website..."):
                try:
                    # Collect and analyze data
                    collected_data = asyncio.run(self.data_collector.collect_all_data(url))
                    report_data = self.report_generator.generate_report(collected_data)
                    
                    # Display results
                    self._display_results(report_data)
                    
                except Exception as e:
                    st.error(f"Error analyzing website: {str(e)}")

    def _display_results(self, data: Dict[str, Any]):
        """Display analysis results."""
        # Overview metrics
        MetricsDisplay.show_overview(data.get('overview', {}))
        
        # Technical Analysis
        ReportDisplay.show_technical_analysis(
            data.get('technical_analysis', {})
        )
        
        # Backlink Analysis
        ReportDisplay.show_backlink_analysis(
            data.get('backlinks', {})
        )
        
        # Issues and Recommendations
        ReportDisplay.show_issues_table(
            data.get('recommendations', [])
        )
        
        # Export options
        if st.button("Download Report (PDF)"):
            pdf_report = self.report_generator.generate_pdf(data)
            st.download_button(
                label="Download PDF",
                data=pdf_report,
                file_name="seo_report.pdf",
                mime="application/pdf"
            )

if __name__ == "__main__":
    # Initialize app with dependencies
    from api.moz_api import MozClient
    from scraper.web_scraper import SEOScraper
    from data.cache import DataCache
    from data.collector import DataCollector
    from data.aggregator import DataAggregator
    from reports.generator import ReportGenerator
    from api.rate_limiter import RateLimiter

    # Instantiate dependencies
    rate_limiter = RateLimiter()
    moz_client = MozClient(token=os.getenv("MOZ_TOKEN"), rate_limiter=rate_limiter)
    scraper = SEOScraper()
    cache = DataCache()
    data_collector = DataCollector(moz_client, scraper, cache)
    report_generator = ReportGenerator()

    # Run the app
    app = SEOApp(data_collector, report_generator)
    app.run()
