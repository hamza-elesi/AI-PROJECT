# import sys
# from pathlib import Path
# import streamlit as st
# from src.data.collector import DataCollector
# from src.reports.generator import ReportGenerator
# from streamlit.components.metrics import MetricsDisplay
# from streamlit.components.report import ReportDisplay
# from dotenv import load_dotenv
# import asyncio
# import os

# # Add project root to Python path
# project_root = Path(__file__).parent  # Parent of "streamlit" and "src"
# sys.path.append(str(project_root / "streamlit"))
# sys.path.append(str(project_root / "src"))

# # Load environment variables
# load_dotenv()


# class SEOApp:
#     def __init__(self, data_collector, report_generator):
#         """Initialize the SEO app with its dependencies."""
#         self.data_collector = data_collector
#         self.report_generator = report_generator
#         self.setup_page()

#     def setup_page(self):
#         """Configure Streamlit page settings."""
#         st.set_page_config(
#             page_title="SEO Analysis Tool",
#             page_icon="🌐",
#             layout="wide",
#         )

#     def run(self):
#         """Main app execution."""
#         st.title("SEO Analysis Tool")
#         url = st.text_input("Enter the website URL", placeholder="https://example.com")

#         if url:
#             with st.spinner("Analyzing website..."):
#                 try:
#                     collected_data = asyncio.run(self.data_collector.collect_all_data(url))
#                     report_data = self.report_generator.generate_report(collected_data)
#                     self._display_results(report_data)
#                 except Exception as e:
#                     st.error(f"Error analyzing website: {str(e)}")

#     def _display_results(self, data):
#         """Display analysis results."""
#         # Overview metrics
#         MetricsDisplay.show_overview(data.get("overview", {}))

#         # Technical Analysis
#         ReportDisplay.show_technical_analysis(data.get("technical_analysis", {}))

#         # Backlink Analysis
#         ReportDisplay.show_backlink_analysis(data.get("backlinks", {}))

#         # Issues and Recommendations
#         ReportDisplay.show_issues_table(data.get("recommendations", []))

#         # Export options
#         if st.button("Download Report (PDF)"):
#             pdf_report = self.report_generator.generate_pdf(data)
#             st.download_button(
#                 "Download PDF", pdf_report, "seo_report.pdf", "application/pdf"
#             )


# if __name__ == "__main__":
#     # Initialize app with dependencies
#     from src.api.moz_api import MozClient
#     from src.scraper.web_scraper import SEOScraper
#     from src.data.cache import DataCache
#     from src.data.collector import DataCollector
#     from src.reports.generator import ReportGenerator
#     from src.api.rate_limiter import RateLimiter

#     # Instantiate dependencies
#     rate_limiter = RateLimiter()
#     moz_client = MozClient(api_token=os.getenv("MOZ_TOKEN"), rate_limiter=rate_limiter)
#     scraper = SEOScraper()
#     cache = DataCache()
#     data_collector = DataCollector(moz_client, scraper, cache)
#     report_generator = ReportGenerator()

#     # Run the app
#     app = SEOApp(data_collector, report_generator)
#     app.run()
import os
import sys
print(os.path.dirname(sys.executable))