from typing import Dict, Any, List
from fpdf import FPDF
from datetime import datetime

class EnhancedReportGenerator:
    """Generates enhanced SEO reports with AI insights."""

    def __init__(self):
        self.pdf = None

    def generate_report(self, data: Dict[str, Any], enhanced_insights: Dict[str, Any]) -> bytes:
        """Generate a complete SEO report with enhanced insights."""
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_auto_page_break(auto=True, margin=15)

        # Generate report sections
        self._add_title_section()
        self._add_executive_summary(enhanced_insights)
        self._add_metrics_section(data)
        self._add_enhanced_technical_section(data, enhanced_insights)
        self._add_enhanced_content_section(data, enhanced_insights)
        self._add_enhanced_backlink_section(data, enhanced_insights)
        self._add_ai_insights_section(enhanced_insights)
        self._add_recommendations_section(enhanced_insights)

        return self.pdf.output(dest='S')  # ✅ Return correct bytes

    def _add_title_section(self):
        """Add the title and date to the report."""
        self.pdf.set_font("Arial", "B", 16)
        self.pdf.cell(0, 10, "SEO Analysis Report", ln=True, align="C")
        date = datetime.now().strftime("%Y-%m-%d")
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(0, 10, f"Date: {date}", ln=True, align="R")

    def _add_executive_summary(self, enhanced_insights: Dict[str, Any]):
        """Add an executive summary of the SEO report."""
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.cell(0, 10, "Executive Summary", ln=True)

        summary = enhanced_insights.get("summary", {})
        self.pdf.set_font("Arial", "", 12)

        if not summary:
            self.pdf.cell(0, 10, "No executive summary available.", ln=True)
        else:
            for key, value in summary.items():
                self.pdf.cell(0, 10, f"{key}: {value}", ln=True)

    def _add_metrics_section(self, data: Dict[str, Any]):
        """Add an overview of SEO metrics."""
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.cell(0, 10, "Metrics Overview", ln=True)

        metrics = data.get("moz_data", {}).get("metrics", {})
        self.pdf.set_font("Arial", "", 12)

        if not metrics:
            self.pdf.cell(0, 10, "No metrics available.", ln=True)
        else:
            for key, value in metrics.items():
                self.pdf.cell(0, 10, f"{key}: {value}", ln=True)

    def _add_enhanced_technical_section(self, data: Dict[str, Any], enhanced_insights: Dict[str, Any]):
        """Add technical SEO analysis insights."""
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.cell(0, 10, "Technical Analysis", ln=True)

        technical_insights = enhanced_insights.get("technical_insights", [])
        self._add_insights(technical_insights)

    def _add_enhanced_content_section(self, data: Dict[str, Any], enhanced_insights: Dict[str, Any]):
        """Add content analysis insights."""
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.cell(0, 10, "Content Analysis", ln=True)

        content_insights = enhanced_insights.get("content_insights", [])
        self._add_insights(content_insights)

    def _add_enhanced_backlink_section(self, data: Dict[str, Any], enhanced_insights: Dict[str, Any]):
        """Add backlink analysis insights."""
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.cell(0, 10, "Backlink Analysis", ln=True)

        backlink_insights = enhanced_insights.get("backlink_insights", [])
        self._add_insights(backlink_insights)

    def _add_ai_insights_section(self, enhanced_insights: Dict[str, Any]):
        """Add AI-generated strategic recommendations."""
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.cell(0, 10, "AI Insights", ln=True)

        strategic_insights = enhanced_insights.get("strategic_recommendations", [])
        self._add_insights(strategic_insights)

    def _add_recommendations_section(self, enhanced_insights: Dict[str, Any]):
        """Add AI-powered SEO recommendations."""
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.cell(0, 10, "Recommendations", ln=True)

        recommendations = enhanced_insights.get("priority_actions", [])
        self._add_insights(recommendations)

    def _add_insights(self, insights: List[Dict[str, Any]]):
        """Helper method to add insights to the report."""
        self.pdf.set_font("Arial", "", 12)

        if not insights:
            self.pdf.cell(0, 10, "No insights available.", ln=True)
        else:
            for insight in insights:
                self.pdf.cell(0, 10, f"• {insight.get('recommendation', 'No recommendation')}", ln=True)
                self.pdf.multi_cell(0, 6, f"{insight.get('description', 'No details provided.')}", ln=True)
                self.pdf.ln(2)  # Space between insights
