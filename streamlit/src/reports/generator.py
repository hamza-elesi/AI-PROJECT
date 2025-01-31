# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.units import inch
# from typing import Dict, Any
# from io import BytesIO
# from src.reports.translations import DutchTranslator


# class ReportGenerator:
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

from typing import Dict, Any
from fpdf import FPDF
from datetime import datetime
from .translations import DutchTranslator

class ReportGenerator:
    """Generates SEO analysis reports in Dutch"""
    
    def __init__(self):
        self.translations = DutchTranslator()
        self.pdf = None

    def generate_report(self, data: Dict[str, Any]) -> bytes:
        print("Starting report generation...")
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_auto_page_break(auto=True, margin=15)

        try:
            # Basic metrics section
            self._add_metrics_section(data['overview'])
            print("Metrics added")

            # Technical SEO section
            self._add_technical_section(data['scraped_data'])
            print("Technical section added")

            # Content Analysis
            self._add_content_section(data['scraped_data'])
            print("Content section added")

            # Backlinks Analysis
            self._add_backlink_section(data['moz_data'])
            print("Backlink section added")

            # Recommendations based on analysis
            self._add_recommendations_section(data)
            print("Recommendations added")

            return self.pdf.output(dest='S').decode('latin1')

        except Exception as e:
            print(f"Error in report generation: {str(e)}")
            raise e

        # return self.pdf.output(dest='S').decode('latin1')

    def _add_title_section(self):
        """Add report title and introduction"""
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.cell(0, 10, "SEO Analyse Rapport", ln=True, align='C')
        self.pdf.ln(5)
        
        # Add date
        self.pdf.set_font('Arial', '', 10)
        current_date = datetime.now().strftime("%d-%m-%Y")
        self.pdf.cell(0, 10, f"Datum: {current_date}", ln=True, align='R')
        self.pdf.ln(5)

        # Add introduction
        self.pdf.set_font('Arial', '', 11)
        self.pdf.multi_cell(0, 5, self.translations.get_description('intro'))
        self.pdf.ln(10)

    def _add_metrics_section(self, data: Dict[str, Any]):
        """Add SEO metrics section"""
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.cell(0, 10, "SEO-Metrics & Overzicht", ln=True)
        
        metrics = [
            ["SEO-metric", "Waarde", "Beoordeling"],
            ["Domain Authority", str(data.get('domain_authority', 0)), self._get_rating(data.get('domain_authority', 0))],
            ["Page Authority", str(data.get('page_authority', 0)), self._get_rating(data.get('page_authority', 0))],
            ["Backlinks", str(data.get('backlinks', 0)), self._get_rating(data.get('backlinks', 0))]
        ]
        
        self._create_table(metrics)

    def _add_technical_section(self, data: Dict[str, Any]):
        """Add technical SEO analysis section"""
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.cell(0, 10, "Technische SEO Analyse", ln=True)
        
        tech_data = data.get('technical_seo', {})
        issues = self._analyze_technical_issues(tech_data)
        
        self._create_table([
            ["Probleem", "Impact", "Aanbeveling"],
            *issues
        ])

    def _add_content_section(self, data: Dict[str, Any]):
        """Add content analysis section"""
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.cell(0, 10, "Content Analyse", ln=True)
        
        content_data = data.get('content', {})
        self._create_table([
            ["Aspect", "Status", "Aanbeveling"],
            *self._analyze_content_issues(content_data)
        ])

    def _add_backlink_section(self, data: Dict[str, Any]):
        """Add backlink analysis section"""
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.cell(0, 10, "Backlink Analyse", ln=True)
        
        backlink_data = data.get('backlinks', {})
        self._create_table([
            ["Metric", "Waarde", "Aanbeveling"],
            *self._analyze_backlinks(backlink_data)
        ])

    def _add_recommendations_section(self, data: Dict[str, Any]):
        """Add recommendations and cost estimates section"""
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.cell(0, 10, "SEO Aanbevelingen & Kosten", ln=True)
        
        self._create_table([
            ["SEO Taak", "Prioriteit", "Tijd", "Kosten"],
            ["Meta-beschrijvingen toevoegen", "Hoog", "2-3 uur", "$100-150"],
            ["H1-tags corrigeren", "Hoog", "1-2 uur", "$75-125"],
            ["Laadtijd optimaliseren", "Hoog", "3-4 uur", "$150-200"],
            ["Content uitbreiden", "Medium", "4-6 uur", "$200-300"],
            ["Backlink profiel verbeteren", "Medium", "Doorlopend", "Op aanvraag"]
        ])

    def _add_conclusion_section(self):
        """Add conclusion and next steps"""
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.cell(0, 10, "Conclusie en Volgende Stappen", ln=True)
        
        self.pdf.set_font('Arial', '', 11)
        self.pdf.multi_cell(0, 5, self.translations.get_description('conclusion'))
        
        # Add next steps
        self.pdf.ln(5)
        steps = [
            "Technische SEO issues oplossen",
            "Contentstrategie verbeteren",
            "Backlinks verkrijgen en monitoren",
            "Regelmatige SEO-audits uitvoeren"
        ]
        
        for step in steps:
            self.pdf.cell(0, 8, f" {step}", ln=True)

    def _create_table(self, data: list):
        """Create a formatted table in the PDF"""
        # Calculate column widths
        col_width = self.pdf.w / len(data[0]) - 10
        
        # Headers
        self.pdf.set_font('Arial', 'B', 10)
        for header in data[0]:
            self.pdf.cell(col_width, 7, header, 1)
        self.pdf.ln()
        
        # Data
        self.pdf.set_font('Arial', '', 10)
        for row in data[1:]:
            for item in row:
                self.pdf.cell(col_width, 6, str(item), 1)
            self.pdf.ln()
        
        self.pdf.ln(5)

    def _get_rating(self, value: int) -> str:
        """Get rating based on value"""
        if value >= 70:
            return "Goed"
        elif value >= 40:
            return "Gemiddeld"
        return "Verbetering nodig"

    def _analyze_technical_issues(self, data: Dict[str, Any]) -> list:
        """Analyze technical SEO issues"""
        issues = []
        # Add your technical analysis logic here
        return issues

    def _analyze_content_issues(self, data: Dict[str, Any]) -> list:
        """Analyze content issues"""
        issues = []
        # Add your content analysis logic here
        return issues

    def _analyze_backlinks(self, data: Dict[str, Any]) -> list:
        """Analyze backlink profile"""
        analysis = []
        # Add your backlink analysis logic here
        return analysis