from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from typing import Dict, Any
from io import BytesIO
from src.reports.translations import DutchTranslator


class ReportGenerator:
    def __init__(self):
        self.translator = DutchTranslator()

    def generate_pdf(self, data: Dict[str, Any]) -> bytes:
        """Generate a structured and formatted PDF report with automatic page breaks and text wrapping."""
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setTitle(self.translator.translate("seo_analysis_report"))

        y_position = 750  # Start position
        line_spacing = 20
        margin_bottom = 50  # Bottom margin limit
        max_line_width = 500  # Maximum width for text before wrapping

        def check_new_page(y_pos):
            """Checks if a new page is needed and adds one if necessary."""
            if y_pos <= margin_bottom:
                pdf.showPage()  # Save current page
                pdf.setFont("Helvetica", 10)  # Reset font
                return 750  # Reset Y position for the new page
            return y_pos

        def wrap_text(text, max_width):
            """Splits text into multiple lines if it's too long."""
            words = text.split()
            lines = []
            current_line = ""

            for word in words:
                test_line = current_line + " " + word if current_line else word
                if stringWidth(test_line, "Helvetica", 10) < max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word  # Start new line with current word

            if current_line:
                lines.append(current_line)

            return lines

        def add_heading(text, y_pos):
            """Draws a heading in the PDF"""
            y_pos = check_new_page(y_pos)
            pdf.setFont("Helvetica-Bold", 14)
            pdf.setFillColor(colors.darkblue)
            pdf.drawString(50, y_pos, text)
            return y_pos - 30

        def add_text(text, y_pos):
            """Draws text and wraps it automatically"""
            y_pos = check_new_page(y_pos)
            pdf.setFont("Helvetica", 10)
            pdf.setFillColor(colors.black)

            lines = wrap_text(text, max_line_width)
            for line in lines:
                y_pos = check_new_page(y_pos)
                pdf.drawString(60, y_pos, line)
                y_pos -= line_spacing

            return y_pos

        def add_table(headers, data, y_pos):
            """Creates a simple table"""
            y_pos = check_new_page(y_pos)
            pdf.setFont("Helvetica-Bold", 10)
            pdf.setFillColor(colors.darkgray)
            pdf.drawString(60, y_pos, " | ".join(headers))
            pdf.setFont("Helvetica", 10)
            pdf.setFillColor(colors.black)
            y_pos -= 20
            for row in data:
                y_pos = check_new_page(y_pos)
                pdf.drawString(60, y_pos, " | ".join(str(item) for item in row))
                y_pos -= 20
            return y_pos - 10

        # 1. General Report Overview
        y_position = add_heading(self.translator.translate("seo_analysis_report"), y_position)
        y_position = add_text(
            "Dit rapport geeft een gedetailleerd overzicht van de SEO-prestaties van uw website.",
            y_position,
        )

        # 2. SEO Performance Overview (Moz Metrics)
        y_position = add_heading(self.translator.translate("website_seo_performance"), y_position)
        moz_data = data.get("moz_data", {}).get("metrics", {})

        metrics_table = [
            [self.translator.translate("domain_authority"), moz_data.get("domain_authority", "N/A")],
            [self.translator.translate("page_authority"), moz_data.get("page_authority", "N/A")],
            [self.translator.translate("total_links"), moz_data.get("total_links", "N/A")],
            [self.translator.translate("linking_domains"), moz_data.get("linking_domains", "N/A")],
            [self.translator.translate("spam_score"), moz_data.get("spam_score", "N/A")],
        ]
        y_position = add_table(["SEO Metric", "Waarde"], metrics_table, y_position)

        # 3. Technical SEO Analysis
        y_position = add_heading(self.translator.translate("technical_seo_check"), y_position)
        scraped_data = data.get("scraped_data", {})
        tech_analysis_table = [
            [self.translator.translate("meta_tags"), scraped_data.get("meta_tags", {}).get("title", "N/A")],
            [self.translator.translate("missing_meta"), "Hoog" if not scraped_data.get("meta_tags", {}).get("meta_description") else "Laag"],
            [self.translator.translate("image_optimization"), scraped_data.get("images", {}).get("missing_alt", "N/A")],
            [self.translator.translate("has_canonical"), scraped_data.get("technical", {}).get("has_canonical", "N/A")],
        ]
        y_position = add_table(["Technisch Probleem", "Impact"], tech_analysis_table, y_position)

        # 4. Content Analysis
        y_position = add_heading(self.translator.translate("content_analysis"), y_position)
        content_data = scraped_data.get("content", {})
        content_table = [
            [self.translator.translate("word_count"), content_data.get("word_count", "N/A")],
            [self.translator.translate("paragraphs"), content_data.get("paragraphs", "N/A")],
            [self.translator.translate("has_structured_data"), content_data.get("has_structured_data", "N/A")],
        ]
        y_position = add_table(["Content Metric", "Waarde"], content_table, y_position)

        # 5. Backlink Analysis
        y_position = add_heading(self.translator.translate("backlink_profile"), y_position)
        backlinks_table = [
            [self.translator.translate("total_links"), moz_data.get("total_links", "N/A")],
            [self.translator.translate("linking_domains"), moz_data.get("linking_domains", "N/A")],
            [self.translator.translate("spam_score"), moz_data.get("spam_score", "N/A")],
        ]
        y_position = add_table(["Backlink Metric", "Waarde"], backlinks_table, y_position)

        # 6. Recommended Improvements & Cost Estimation
        y_position = add_heading(self.translator.translate("seo_recommendations"), y_position)
        improvement_table = [
            [self.translator.translate("missing_meta"), "Hoog", "2-3 uur", "€100-150"],
            [self.translator.translate("image_optimization"), "Medium", "1-2 uur", "€75-125"],
            [self.translator.translate("content_analysis"), "Medium", "4-6 uur", "€200-300"],
            [self.translator.translate("backlink_profile"), "Doorlopend", "Afhankelijk", "Op aanvraag"],
        ]
        y_position = add_table(["SEO Taak", "Prioriteit", "Tijd", "Kosten"], improvement_table, y_position)

        # 7. Conclusion & Next Steps
        y_position = add_heading(self.translator.translate("conclusion"), y_position)
        y_position = add_text(
            "Uw website heeft verschillende optimalisatiemogelijkheden. "
            "We raden aan om te beginnen met technische verbeteringen en contentoptimalisatie "
            "voor de grootste impact.",
            y_position,
        )

        # Next Steps
        y_position = add_heading(self.translator.translate("next_steps"), y_position)
        y_position = add_text(
            "Actiepunten: Begin met technische verbeteringen en monitor de prestaties van uw backlinks en contentoptimalisatie.",
            y_position,
        )

        # Save the PDF
        pdf.save()
        buffer.seek(0)
        return buffer.getvalue()
