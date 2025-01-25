from data.colllector import DataCollector
from reports.generator import ReportGenerator
import streamlit as st
from typing import Dict, Any
from .config import Config
from .components.metrics import MetricsDisplay
from .components.report import ReportDisplay

class SEOApp:
    def __init__(self, data_collector, report_generator):
        self.data_collector = data_collector
        self.report_generator = report_generator
        Config.setup_page()

    def run(self):
        """Main app execution"""
        st.title("SEO Analyse Tool")
        
        # URL Input
        url = st.text_input(
            "Voer website URL in",
            placeholder="https://example.com"
        )
        
        if url:
            with st.spinner("Analyzing website..."):
                try:
                    # Collect and analyze data
                    collected_data = self.data_collector.collect_all_data(url)
                    report_data = self.report_generator.generate_report(collected_data)
                    
                    # Display results
                    self._display_results(report_data)
                    
                except Exception as e:
                    st.error(f"Error analyzing website: {str(e)}")

    def _display_results(self, data: Dict[str, Any]):
        """Display analysis results"""
        # Overview metrics
        MetricsDisplay.show_overview(data.get('overview', {}))
        
        # Search Console metrics
        MetricsDisplay.show_search_console_metrics(
            data.get('performance_metrics', {})
        )
        
        # Technical Analysis
        ReportDisplay.show_technical_analysis(
            data.get('technical_analysis', {})
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
    app = SEOApp(DataCollector, ReportGenerator)
    app.run()