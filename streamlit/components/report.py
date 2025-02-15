# import asyncio
# import streamlit as st
# from components.metrics import MetricsDisplay
# from components.report import ReportDisplay
# from src.data.collector import DataCollector
# from src.reports.generator import EnhancedReportGenerator
# from src.api.moz_api import MozClient
# from src.scraper.web_scraper import SEOScraper
# from src.data.cache import DataCache
# from src.api.rate_limiter import RateLimiter
# from src.ai.insights.generator import AIInsightsGenerator
# import os
# from dotenv import load_dotenv
# # __import__('pysqlite3')
# # import sys
# # sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# # Load environment variables
# load_dotenv(override=True)

# class SEOApp:
#     def __init__(self, data_collector, report_generator):
#         self.data_collector = data_collector
#         self.report_generator = report_generator
#         self.ai_generator = AIInsightsGenerator()

#     async def analyze_website(self, url):
#         """Runs SEO analysis asynchronously."""
#         collected_data = await self.data_collector.collect_all_data(url)
#         enhanced_insights = await self.ai_generator.generate_insights(collected_data)

#         # ✅ Debugging: Ensure Data is Collected
#         print("🟢 MOZ Data (Backlink Check):", collected_data.get("moz_data", {}))
#         print("🟢 AI Insights Generated:", enhanced_insights)

#         return collected_data, enhanced_insights

#     def run(self):
#         """Run the Streamlit SEO analysis tool."""
#         st.title("🔎 SEO Analysis Tool")

#         # ✅ Initialize session state variables safely
#         for key in ["url", "collected_data", "enhanced_insights", "pdf_ready", "pdf_data"]:
#             if key not in st.session_state:
#                 st.session_state[key] = None  

#         # 🔹 Input field for URL
#         url = st.text_input(
#             "Enter the website URL",
#             placeholder="https://example.com",
#             value=st.session_state.url,
#             key="url_input",
#         )

#         # 🔹 Analyze button
#         if st.button("Analyze"):
#             if url:
#                 st.session_state.url = url
#                 with st.spinner("🔄 Analyzing website..."):
#                     try:
#                         collected_data, enhanced_insights = asyncio.run(self.analyze_website(url))  # ✅ FIX: Use asyncio.run() to avoid conflicts

#                         # ✅ Store data in session state
#                         st.session_state.collected_data = collected_data
#                         st.session_state.enhanced_insights = enhanced_insights
#                         st.session_state.pdf_ready = False
#                         st.success("✅ Website analyzed successfully!")

#                     except Exception as e:
#                         st.error(f"❌ Error analyzing website: {str(e)}")
#             else:
#                 st.error("⚠️ Please enter a valid URL!")

#         # 🔹 Display analysis results
#         if st.session_state.collected_data and st.session_state.enhanced_insights:
#             self._display_results(
#                 st.session_state.collected_data, st.session_state.enhanced_insights
#             )

#     def _display_results(self, data, enhanced_insights):
#         """Display analysis results in Streamlit."""

#         # 🔹 SEO Metrics Overview
#         st.subheader("📊 SEO Metrics Overview")
#         MetricsDisplay.show_overview(data.get("overview", {}))

#         # 🔹 Technical SEO Analysis
#         st.subheader("🛠️ Technical SEO Analysis")
#         ReportDisplay.show_technical_analysis(data.get("scraped_data", {}))

#         # 🔹 AI-Generated Technical Insights
#         technical_insights = enhanced_insights.get("technical_insights", [])
#         if technical_insights:
#             st.subheader("🤖 AI-Generated Technical Insights")
#             for insight in technical_insights:
#                 st.write(f"**{insight.get('recommendation', 'No Title')}**")
#         else:
#             st.write("⚠️ No AI-generated technical insights available.")

#         # 🔹 Backlink Analysis (Fixed - Removed Duplicate)
#         if "moz_data" in data and "metrics" in data["moz_data"]:
#             st.subheader("🔗 Backlink Analysis")
#             ReportDisplay.show_backlink_analysis(data["moz_data"]["metrics"])

#         # 🔹 AI-Generated Backlink Insights (Ensured to Show Properly)
#         backlink_insights = enhanced_insights.get("backlink_insights", [])
#         if backlink_insights:
#             st.subheader("📡 AI-Generated Backlink Insights")
#             for insight in backlink_insights:
#                 st.write(f"**{insight.get('recommendation', 'No Title')}**")
#         else:
#             st.write("⚠️ No AI-enhanced backlink insights available.")

#         # 🔹 AI-Generated Strategic Recommendations
#         st.subheader("🧠 AI-Generated Strategic Recommendations")
#         strategic_insights = enhanced_insights.get("strategic_recommendations", [])
#         if strategic_insights:
#             for insight in strategic_insights:
#                 st.write(f"**{insight.get('recommendation', 'No Title')}**")
#         else:
#             st.write("⚠️ No AI-generated strategic recommendations available.")

#         # 🔹 AI-Generated Priority Actions
#         st.subheader("🔥 AI-Generated Priority Actions")
#         priority_actions = enhanced_insights.get("priority_actions", [])
#         if priority_actions:
#             for action in priority_actions:
#                 st.write(f"**{action.get('recommendation', 'No Title')}**")
#         else:
#             st.write("⚠️ No AI-generated priority actions available.")

#         # 🔹 Generate PDF Report
#         if st.button("📄 Generate Report"):
#             with st.spinner("Generating report..."):
#                 try:
#                     pdf_report = self.report_generator.generate_report(data, enhanced_insights)
#                     pdf_bytes = bytes(pdf_report) if isinstance(pdf_report, bytearray) else pdf_report

#                     # ✅ Store report data
#                     st.session_state.pdf_ready = True
#                     st.session_state.pdf_data = pdf_bytes
#                     st.success("✅ Report generated successfully!")
#                 except Exception as e:
#                     st.error(f"❌ Error generating report: {str(e)}")

#         # 🔹 Download PDF Report
#         if st.session_state.pdf_ready and st.session_state.pdf_data:
#             st.download_button(
#                 label="📥 Download PDF Report",
#                 data=st.session_state.pdf_data,
#                 file_name="seo_analysis_report.pdf",
#                 mime="application/pdf",
#             )

# if __name__ == "__main__":
#     rate_limiter = RateLimiter()
#     moz_client = MozClient(api_token=os.getenv("MOZ_TOKEN"), rate_limiter=rate_limiter)
#     scraper = SEOScraper()
#     cache = DataCache()
#     data_collector = DataCollector(moz_client, scraper, cache)
#     report_generator = EnhancedReportGenerator()

#     app = SEOApp(data_collector, report_generator)
#     app.run()


import asyncio
import streamlit as st
from components.metrics import MetricsDisplay
from components.report import ReportDisplay
from src.data.collector import DataCollector
from src.reports.generator import EnhancedReportGenerator
from src.api.moz_api import MozClient
from src.scraper.web_scraper import SEOScraper
from src.data.cache import DataCache
from src.api.rate_limiter import RateLimiter
from src.ai.insights.generator import AIInsightsGenerator
import os
from dotenv import load_dotenv
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Load environment variables
load_dotenv(override=True)

class SEOApp:
    def __init__(self, data_collector, report_generator):
        self.data_collector = data_collector
        self.report_generator = report_generator
        self.ai_generator = AIInsightsGenerator()

    async def analyze_website(self, url):
        """Runs SEO analysis asynchronously."""
        collected_data = await self.data_collector.collect_all_data(url)
        enhanced_insights = await self.ai_generator.generate_insights(collected_data)

        # ✅ Debugging: Ensure Data is Collected
        print("🟢 MOZ Data (Backlink Check):", collected_data.get("moz_data", {}))
        print("🟢 AI Insights Generated:", enhanced_insights)

        return collected_data, enhanced_insights

    def run(self):
        """Run the Streamlit SEO analysis tool."""
        st.title("🔎 SEO Analysis Tool")

        # ✅ Initialize session state variables safely
        for key in ["url", "collected_data", "enhanced_insights", "pdf_ready", "pdf_data"]:
            if key not in st.session_state:
                st.session_state[key] = None  

        # 🔹 Input field for URL
        url = st.text_input(
            "Enter the website URL",
            placeholder="https://example.com",
            value=st.session_state.url,
            key="url_input",
        )

        # 🔹 Analyze button
        if st.button("Analyze"):
            if url:
                st.session_state.url = url
                with st.spinner("🔄 Analyzing website..."):
                    try:
                        collected_data, enhanced_insights = asyncio.run(self.analyze_website(url))  # ✅ FIX: Use asyncio.run() to avoid conflicts

                        # ✅ Store data in session state
                        st.session_state.collected_data = collected_data
                        st.session_state.enhanced_insights = enhanced_insights
                        st.session_state.pdf_ready = False
                        st.success("✅ Website analyzed successfully!")

                    except Exception as e:
                        st.error(f"❌ Error analyzing website: {str(e)}")
            else:
                st.error("⚠️ Please enter a valid URL!")

        # 🔹 Display analysis results
        if st.session_state.collected_data and st.session_state.enhanced_insights:
            self._display_results(
                st.session_state.collected_data, st.session_state.enhanced_insights
            )

    def _display_results(self, data, enhanced_insights):
        st.subheader("📊 SEO Metrics Overview")
        MetricsDisplay.show_overview(data.get("overview", {}))

        st.subheader("🛠️ Technical SEO Analysis")
        ReportDisplay.show_technical_analysis(data.get("scraped_data", {}))

        ReportDisplay.show_backlink_analysis(data.get("backlink_data", {}).get("metrics", {}))

        ReportDisplay.show_content_analysis(data.get("content_data", {}).get("metrics", {}))

        # 🔹 AI-Generated Technical Insights
        technical_insights = enhanced_insights.get("technical_insights", [])
        if technical_insights:
            st.subheader("🤖 AI-Generated Technical Insights")
            for insight in technical_insights:
                st.write(f"**{insight.get('recommendation', 'No Title')}**")
        else:
            st.write("⚠️ No AI-generated technical insights available.")

        # 🔹 Backlink Analysis (Fixed - Removed Duplicate)
        if "moz_data" in data and "metrics" in data["moz_data"]:
            st.subheader("🔗 Backlink Analysis")
            ReportDisplay.show_backlink_analysis(data["moz_data"]["metrics"])

        # 🔹 AI-Generated Backlink Insights (Ensured to Show Properly)
        backlink_insights = enhanced_insights.get("backlink_insights", [])
        if backlink_insights:
            st.subheader("📡 AI-Generated Backlink Insights")
            for insight in backlink_insights:
                st.write(f"**{insight.get('recommendation', 'No Title')}**")
        else:
            st.write("⚠️ No AI-enhanced backlink insights available.")

        # 🔹 AI-Generated Strategic Recommendations
        st.subheader("🧠 AI-Generated Strategic Recommendations")
        strategic_insights = enhanced_insights.get("strategic_recommendations", [])
        if strategic_insights:
            for insight in strategic_insights:
                st.write(f"**{insight.get('recommendation', 'No Title')}**")
        else:
            st.write("⚠️ No AI-generated strategic recommendations available.")

        # 🔹 AI-Generated Priority Actions
        st.subheader("🔥 AI-Generated Priority Actions")
        priority_actions = enhanced_insights.get("priority_actions", [])
        if priority_actions:
            for action in priority_actions:
                st.write(f"**{action.get('recommendation', 'No Title')}**")
        else:
            st.write("⚠️ No AI-generated priority actions available.")

        # 🔹 Generate PDF Report
        if st.button("📄 Generate Report"):
            with st.spinner("Generating report..."):
                try:
                    pdf_report = self.report_generator.generate_report(data, enhanced_insights)
                    pdf_bytes = bytes(pdf_report) if isinstance(pdf_report, bytearray) else pdf_report

                    # ✅ Store report data
                    st.session_state.pdf_ready = True
                    st.session_state.pdf_data = pdf_bytes
                    st.success("✅ Report generated successfully!")
                except Exception as e:
                    st.error(f"❌ Error generating report: {str(e)}")

        # 🔹 Download PDF Report
        if st.session_state.pdf_ready and st.session_state.pdf_data:
            st.download_button(
                label="📥 Download PDF Report",
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
    report_generator = EnhancedReportGenerator()

    app = SEOApp(data_collector, report_generator)
    app.run()
