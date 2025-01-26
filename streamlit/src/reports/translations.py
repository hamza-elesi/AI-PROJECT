from typing import Dict, Any

class DutchTranslator:
    """Handle Dutch translations for the report"""
    
    def __init__(self):
        self.translations = {
            # SEO Metrics
            'seo_score': 'SEO Score',
            'domain_authority': 'Domain Autoriteit',
            'page_authority': 'Pagina Autoriteit',
            'backlinks': 'Backlinks',
            
            # Technical SEO
            'technical_seo': 'Technische SEO',
            'meta_tags': 'Meta Tags',
            'missing_meta': 'Ontbrekende Meta Tags',
            'image_optimization': 'Afbeeldingsoptimalisatie',
            
            # Search Console Metrics
            'clicks': 'Clicks',
            'impressions': 'Impressies',
            'ctr': 'Click Through Rate',
            'position': 'Gemiddelde Positie',
            
            # Priority Levels
            'high': 'Hoog',
            'medium': 'Gemiddeld',
            'low': 'Laag',
            
            # Time and Cost
            'estimated_time': 'Geschatte Tijd',
            'estimated_cost': 'Geschatte Kosten',
            'hours': 'uur',
            
            # Report Sections
            'overview': 'Overzicht',
            'issues': 'Problemen',
            'recommendations': 'Aanbevelingen',
            'content_analysis': 'Content Analyse',
            
            # Common Terms
            'total': 'Totaal',
            'status': 'Status',
            'priority': 'Prioriteit',
            'action_required': 'Actie Vereist'
        }

    def translate(self, key: str) -> str:
        """Get Dutch translation for a key"""
        return self.translations.get(key, key)

    def translate_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Translate dictionary keys to Dutch"""
        return {
            self.translate(k): v 
            for k, v in data.items()
        }