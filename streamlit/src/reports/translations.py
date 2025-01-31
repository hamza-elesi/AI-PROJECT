from typing import Dict, Any

# class DutchTranslator:
#     """Handle Dutch translations for the report"""
    
#     def __init__(self):
#         self.translations = {
#             # General Report
#             'seo_analysis_report': 'SEO Analyse Rapport',
#             'moz_metrics': 'Moz Statistieken',
#             'scraped_data': 'Opgehaalde Gegevens',
#             'generated_by_seo_tool': 'Gegenereerd door SEO Analyse Tool',

#             # SEO Metrics
#             'domain_authority': 'Domein Autoriteit',
#             'page_authority': 'Pagina Autoriteit',
#             'backlinks': 'Backlinks',
#             'total_links': 'Totale Links',
#             'linking_domains': 'Verwijzende Domeinen',
#             'spam_score': 'Spam Score',
#             'last_crawled': 'Laatst Gecrawld',

#             # Technical SEO
#             'technical_seo': 'Technische SEO',
#             'meta_tags': 'Meta Tags',
#             'missing_meta': 'Ontbrekende Meta Tags',
#             'image_optimization': 'Afbeeldingsoptimalisatie',
#             'headings': 'Koppen',
#             'links': 'Links',
#             'content_quality': 'Content Kwaliteit',
#             'word_count': 'Aantal Woorden',
#             'paragraphs': 'Paragrafen',
#             'has_structured_data': 'Bevat Gestructureerde Gegevens',

#             # Search Console Metrics
#             'clicks': 'Clicks',
#             'impressions': 'Impressies',
#             'ctr': 'Click Through Rate',
#             'position': 'Gemiddelde Positie',

#             # Priority Levels
#             'high': 'Hoog',
#             'medium': 'Gemiddeld',
#             'low': 'Laag',

#             # Time and Cost
#             'estimated_time': 'Geschatte Tijd',
#             'estimated_cost': 'Geschatte Kosten',
#             'hours': 'Uren',

#             # Common Terms
#             'overview': 'Overzicht',
#             'issues': 'Problemen',
#             'recommendations': 'Aanbevelingen',
#             'total': 'Totaal',
#             'status': 'Status',
#             'priority': 'Prioriteit',
#             'action_required': 'Actie Vereist'
#         }

#     def translate(self, key: str) -> str:
#         """Get Dutch translation for a key"""
#         return self.translations.get(key, key)

#     def translate_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
#         """Translate dictionary keys to Dutch"""
#         return {
#             self.translate(k): v 
#             for k, v in data.items()
#         }

# src/reports/translations.py

class DutchTranslator:
    """Handles Dutch translations for SEO reports"""
    
    def __init__(self):
        # Main translations dictionary
        self.translations = {
            # Report Titles
            'report_title': 'SEO Analyse Rapport',
            'overview_title': 'Algemeen Overzicht',
            'technical_title': 'Technische SEO Analyse',
            'content_title': 'Content Analyse',
            'backlink_title': 'Backlink Analyse',
            'recommendations_title': 'Aanbevelingen',
            
            # Metrics
            'domain_authority': 'Domein Autoriteit',
            'page_authority': 'Pagina Autoriteit',
            'backlinks': 'Backlinks',
            
            # Ratings
            'good': 'Goed',
            'average': 'Gemiddeld',
            'poor': 'Verbetering nodig',
            
            # Priorities
            'high': 'Hoog',
            'medium': 'Gemiddeld',
            'low': 'Laag'
        }
        
        # Descriptions dictionary
        self.section_descriptions = {
            'intro': """Dit rapport geeft een gedetailleerd overzicht van de SEO-prestaties van uw website. 
                    We analyseren technische SEO, contentoptimalisatie en backlinkprofiel, en geven 
                    aanbevelingen om uw online zichtbaarheid te verbeteren.""",
            
            'technical': """Technische SEO is essentieel om zoekmachines te helpen uw website goed te indexeren 
                        en crawlen. Hieronder vindt u de belangrijkste technische verbeterpunten en aanbevelingen.""",
            
            'content': """Content is de kern van SEO. Het is belangrijk dat uw pagina's goed gestructureerd 
                      en leesbaar zijn voor zowel gebruikers als zoekmachines.""",
            
            'backlinks': """Backlinks zijn een belangrijke SEO-factor. Een sterk backlinkprofiel verhoogt uw 
                        autoriteit en helpt uw positie in zoekmachines.""",
            
            'conclusion': """Op basis van deze analyse hebben we verschillende verbeterpunten geïdentificeerd. 
                         Door deze aanbevelingen te implementeren kunt u de SEO-prestaties van uw website verbeteren."""
        }

    def get_text(self, key: str) -> str:
        """Get translation for a specific key"""
        return self.translations.get(key, key)

    def get_description(self, key: str) -> str:
        """Get description for a specific section"""
        return self.section_descriptions.get(key, '')