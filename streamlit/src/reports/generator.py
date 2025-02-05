# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.units import inch
# from typing import Dict, Any
# from fpdf import FPDF
# from datetime import datetime
# from .translations import DutchTranslator

# class ReportGenerator:
#     """Generates SEO analysis reports in Dutch"""
    
#     def __init__(self):
#         self.translator = DutchTranslator()  # Initialize the translator

#     def generate_pdf(self, data: Dict[str, Any]) -> bytes:
#         """Generate a structured and formatted PDF report from the analysis results."""
#         buffer = BytesIO()
#         pdf = canvas.Canvas(buffer, pagesize=letter)
#         pdf.setTitle("SEO Analyse Rapport")  # Translated Title

#         # Define initial positions for text
#         y_position = 750  # Start from the top of the page
#         line_spacing = 20  # Space between lines

#         # Function to add headings
#         def add_heading(text, y_pos):
#             pdf.setFont("Helvetica-Bold", 14)
#             pdf.setFillColor(colors.darkblue)
#             pdf.drawString(50, y_pos, text)
#             return y_pos - 30  # Move cursor down

#         # Function to add normal text
#         def add_text(text, y_pos):
#             pdf.setFont("Helvetica", 10)
#             pdf.setFillColor(colors.black)
#             pdf.drawString(60, y_pos, text)
#             return y_pos - line_spacing  # Move cursor down

#         # Title
#         y_position = add_heading(self.translator.translate("seo_analysis_report"), y_position)

#         # Moz Metrics Section
#         y_position = add_heading(self.translator.translate("moz_metrics"), y_position)
#         moz_data = data.get("moz_data", {}).get("metrics", {})
#         for key, value in self.translator.translate_dict(moz_data).items():
#             y_position = add_text(f"{key}: {value}", y_position)

#         # Scraped Data Section
#         y_position = add_heading(self.translator.translate("scraped_data"), y_position)
#         scraped_data = data.get("scraped_data", {})

#         # Meta Tags
#         y_position = add_heading(self.translator.translate("meta_tags"), y_position)
#         meta_tags = scraped_data.get("meta_tags", {})
#         for key, value in self.translator.translate_dict(meta_tags).items():
#             y_position = add_text(f"{key}: {value or 'Niet Beschikbaar'}", y_position)

#         # Headings
#         y_position = add_heading(self.translator.translate("headings"), y_position)
#         headings = scraped_data.get("headings", {})
#         for key, value in self.translator.translate_dict(headings).items():
#             y_position = add_text(f"{key}: {value}", y_position)

#         # Images
#         y_position = add_heading(self.translator.translate("image_optimization"), y_position)
#         images = scraped_data.get("images", {})
#         for key, value in self.translator.translate_dict(images).items():
#             y_position = add_text(f"{key}: {value}", y_position)

#         # Links
#         y_position = add_heading(self.translator.translate("links"), y_position)
#         links = scraped_data.get("links", {})
#         for key, value in self.translator.translate_dict(links).items():
#             y_position = add_text(f"{key}: {value}", y_position)

#         # Content Quality
#         y_position = add_heading(self.translator.translate("content_quality"), y_position)
#         content = scraped_data.get("content", {})
#         for key, value in self.translator.translate_dict(content).items():
#             y_position = add_text(f"{key}: {value}", y_position)

#         # Technical Elements
#         y_position = add_heading(self.translator.translate("technical_seo"), y_position)
#         technical = scraped_data.get("technical", {})
#         for key, value in self.translator.translate_dict(technical).items():
#             y_position = add_text(f"{key}: {value}", y_position)

#         # Footer
#         pdf.setFont("Helvetica", 8)
#         pdf.setFillColor(colors.gray)
#         pdf.drawString(50, 50, self.translator.translate("generated_by_seo_tool"))

#         # Save the PDF
#         pdf.save()
#         buffer.seek(0)
#         return buffer.getvalue()
# src/reports/generator.py

from typing import Dict, Any, List
from fpdf import FPDF
from datetime import datetime
from .translations import DutchTranslator

class EnhancedReportGenerator:
    """Generates enhanced SEO reports with AI insights in Dutch"""
    
    def __init__(self):
        self.translations = DutchTranslator()
        self.pdf = None

    def generate_report(self, data: Dict[str, Any], enhanced_insights: Dict[str, Any]) -> bytes:
        """Generate complete SEO report with enhanced insights"""
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
        self._add_implementation_plan(enhanced_insights)

        return self.pdf.output(dest='S').encode('latin1')

    def _add_title_section(self):
        """Add report title and date"""
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.cell(0, 10, "SEO Analyse Rapport", ln=True, align='C')
        
        self.pdf.set_font('Arial', '', 10)
        date = datetime.now().strftime("%d-%m-%Y")
        self.pdf.cell(0, 10, f"Datum: {date}", ln=True, align='R')

    def _add_executive_summary(self, enhanced_insights: Dict[str, Any]):
        """Add executive summary with key findings"""
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.cell(0, 10, "Samenvatting", ln=True)

        summary = enhanced_insights.get('summary', {})
        self.pdf.set_font('Arial', '', 11)
        self._add_summary_table([
            ["Totaal aantal inzichten", str(summary.get('total_insights', 0))],
            ["Kritieke problemen", str(summary.get('critical_issues', 0))],
            ["Snelle verbeteringen", str(summary.get('quick_wins', 0))],
            ["Geschatte totale kosten", str(summary.get('estimated_total_cost', '0'))]
        ])

    def _add_enhanced_technical_section(self, data: Dict[str, Any], enhanced_insights: Dict[str, Any]):
        """Add technical analysis with AI insights"""
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.cell(0, 10, "Technische SEO Analyse", ln=True)

        technical_insights = enhanced_insights.get('technical', [])
        for insight in technical_insights:
            self._add_insight_box(insight)

    def _add_enhanced_content_section(self, data: Dict[str, Any], enhanced_insights: Dict[str, Any]):
        """Add content analysis with AI insights"""
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.cell(0, 10, "Content Analyse", ln=True)

        content_insights = enhanced_insights.get('content', [])
        for insight in content_insights:
            self._add_insight_box(insight)

    def _add_ai_insights_section(self, enhanced_insights: Dict[str, Any]):
        """Add AI-generated insights section"""
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.cell(0, 10, "AI Inzichten", ln=True)

        strategic_insights = enhanced_insights.get('strategic', [])
        for insight in strategic_insights:
            self._add_strategic_insight_box(insight)

    def _add_insight_box(self, insight: Dict[str, Any]):
        """Add formatted insight box"""
        metadata = insight.get('metadata', {})
        
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 8, insight.get('title', ''), ln=True)
        
        self.pdf.set_font('Arial', '', 10)
        self.pdf.multi_cell(0, 6, insight.get('description', ''))
        
        # Add metadata table
        self._add_metadata_table([
            ["Prioriteit", metadata.get('priority', '')],
            ["Impact", f"{metadata.get('impact', 0)*100}%"],
            ["Implementatietijd", metadata.get('implementation_time', '')],
            ["Geschatte kosten", metadata.get('estimated_cost', '')]
        ])

    def _add_strategic_insight_box(self, insight: Dict[str, Any]):
        """Add strategic insight with additional context"""
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 8, insight.get('title', ''), ln=True)
        
        self.pdf.set_font('Arial', '', 10)
        self.pdf.multi_cell(0, 6, insight.get('description', ''))
        
        # Add impact analysis
        self._add_impact_table([
            ["Lange termijn impact", insight.get('long_term_impact', '')],
            ["Concurrentievoordeel", insight.get('competitive_advantage', '')],
            ["Benodigde middelen", insight.get('resource_requirements', '')]
        ])

    def _add_implementation_plan(self, enhanced_insights: Dict[str, Any]):
        """Add implementation plan section"""
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.cell(0, 10, "Implementatieplan", ln=True)

        priorities = enhanced_insights.get('priorities', [])
        for i, action in enumerate(priorities, 1):
            self._add_action_item(i, action)

    def _add_action_item(self, number: int, action: Dict[str, Any]):
        """Add formatted action item"""
        self.pdf.set_font('Arial', 'B', 11)
        self.pdf.cell(0, 8, f"{number}. {action.get('title', '')}", ln=True)
        
        self.pdf.set_font('Arial', '', 10)
        self.pdf.multi_cell(0, 6, action.get('description', ''))
        
        # Add steps if available
        steps = action.get('implementation_steps', [])
        if steps:
            self.pdf.ln(4)
            for step in steps:
                self.pdf.cell(0, 6, f"• {step}", ln=True)

    def _add_table(self, data: List[List[str]], col_width: float = None):
        """Add formatted table"""
        if col_width is None:
            col_width = self.pdf.w / len(data[0]) - 20
            
        for row in data:
            for item in row:
                self.pdf.cell(col_width, 8, str(item), 1)
            self.pdf.ln()

    def _add_summary_table(self, data: List[List[str]]):
        """Add summary table with specific formatting"""
        self._add_table(data, col_width=self.pdf.w/2 - 10)

    def _add_metadata_table(self, data: List[List[str]]):
        """Add metadata table with specific formatting"""
        self._add_table(data, col_width=self.pdf.w/3 - 10)

    def _add_impact_table(self, data: List[List[str]]):
        """Add impact analysis table with specific formatting"""
        self._add_table(data, col_width=self.pdf.w/2 - 10)