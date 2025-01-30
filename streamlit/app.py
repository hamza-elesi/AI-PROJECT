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

        # Initialize session state for URL and data
        if "url" not in st.session_state:
            st.session_state.url = ""
        if "collected_data" not in st.session_state:
            st.session_state.collected_data = None
        if "pdf_ready" not in st.session_state:
            st.session_state.pdf_ready = False

        # Input field for URL
        url = st.text_input(
            "Enter the website URL",
            placeholder="https://example.com",
            value=st.session_state.url,
            key="url_input",
        )

        # Analyze button
        if st.button("Analyze"):
            if url:
                st.session_state.url = url
                with st.spinner("Analyzing website..."):
                    try:
                        collected_data = asyncio.run(self.data_collector.collect_all_data(url))
                        st.session_state.collected_data = collected_data
                        st.session_state.pdf_ready = False
                    except Exception as e:
                        st.error(f"Error analyzing website: {str(e)}")
            else:
                st.error("Please enter a valid URL!")

        # Display analysis results if available
        if st.session_state.collected_data:
            self._display_results(st.session_state.collected_data)

    def _display_results(self, data):
        """Display analysis results."""
        MetricsDisplay.show_overview(data.get("overview", {}))
        ReportDisplay.show_technical_analysis(data.get("scraped_data", {}))
        ReportDisplay.show_backlink_analysis(data.get("moz_data", {}).get("metrics", {}))

        # Generate PDF report
        if st.button("Generate Report"):
            pdf_report = self.report_generator.generate_pdf(data)
            st.session_state.pdf_ready = True
            st.session_state.pdf_data = pdf_report

        # Display download button after generating the report
        if st.session_state.pdf_ready:
            st.download_button(
                label="Export PDF",
                data=st.session_state.pdf_data,
                file_name="seo_analysis_report.pdf",
                mime="application/pdf",
            )


if __name__ == "__main__":
    rate_limiter = RateLimiter()
    moz_client = MozClient(api_token=os.getenv("MOZ_TOKEN"), rate_limiter=rate_limiter)
    scraper = SEOScraper()
    cache = DataCache()
    data_collector = DataCollector(moz_client, scraper, cache)

    # Use the translation-enabled report generator
    report_generator = ReportGenerator()

    app = SEOApp(data_collector, report_generator)
    app.run()
