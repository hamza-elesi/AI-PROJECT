from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from typing import Dict, Any
from fpdf import FPDF
from datetime import datetime
from .translations import DutchTranslator

class ReportGenerator:
    """Generates SEO analysis reports in Dutch"""
    
    def __init__(self):
        self.translator = DutchTranslator()  # Initialize the translator

    def generate_pdf(self, data: Dict[str, Any]) -> bytes:
        """Generate a structured and formatted PDF report from the analysis results."""
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setTitle("SEO Analyse Rapport")  # Translated Title

        # Define initial positions for text
        y_position = 750  # Start from the top of the page
        line_spacing = 20  # Space between lines

        # Function to add headings
        def add_heading(text, y_pos):
            pdf.setFont("Helvetica-Bold", 14)
            pdf.setFillColor(colors.darkblue)
            pdf.drawString(50, y_pos, text)
            return y_pos - 30  # Move cursor down

        # Function to add normal text
        def add_text(text, y_pos):
            pdf.setFont("Helvetica", 10)
            pdf.setFillColor(colors.black)
            pdf.drawString(60, y_pos, text)
            return y_pos - line_spacing  # Move cursor down

        # Title
        y_position = add_heading(self.translator.translate("seo_analysis_report"), y_position)

        # Moz Metrics Section
        y_position = add_heading(self.translator.translate("moz_metrics"), y_position)
        moz_data = data.get("moz_data", {}).get("metrics", {})
        for key, value in self.translator.translate_dict(moz_data).items():
            y_position = add_text(f"{key}: {value}", y_position)

        # Scraped Data Section
        y_position = add_heading(self.translator.translate("scraped_data"), y_position)
        scraped_data = data.get("scraped_data", {})

        # Meta Tags
        y_position = add_heading(self.translator.translate("meta_tags"), y_position)
        meta_tags = scraped_data.get("meta_tags", {})
        for key, value in self.translator.translate_dict(meta_tags).items():
            y_position = add_text(f"{key}: {value or 'Niet Beschikbaar'}", y_position)

        # Headings
        y_position = add_heading(self.translator.translate("headings"), y_position)
        headings = scraped_data.get("headings", {})
        for key, value in self.translator.translate_dict(headings).items():
            y_position = add_text(f"{key}: {value}", y_position)

        # Images
        y_position = add_heading(self.translator.translate("image_optimization"), y_position)
        images = scraped_data.get("images", {})
        for key, value in self.translator.translate_dict(images).items():
            y_position = add_text(f"{key}: {value}", y_position)

        # Links
        y_position = add_heading(self.translator.translate("links"), y_position)
        links = scraped_data.get("links", {})
        for key, value in self.translator.translate_dict(links).items():
            y_position = add_text(f"{key}: {value}", y_position)

        # Content Quality
        y_position = add_heading(self.translator.translate("content_quality"), y_position)
        content = scraped_data.get("content", {})
        for key, value in self.translator.translate_dict(content).items():
            y_position = add_text(f"{key}: {value}", y_position)

        # Technical Elements
        y_position = add_heading(self.translator.translate("technical_seo"), y_position)
        technical = scraped_data.get("technical", {})
        for key, value in self.translator.translate_dict(technical).items():
            y_position = add_text(f"{key}: {value}", y_position)

        # Footer
        pdf.setFont("Helvetica", 8)
        pdf.setFillColor(colors.gray)
        pdf.drawString(50, 50, self.translator.translate("generated_by_seo_tool"))

        # Save the PDF
        pdf.save()
        buffer.seek(0)
        return buffer.getvalue()
