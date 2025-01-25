from typing import Dict, Any
import os
from dotenv import load_dotenv

class Settings:
   """Configuration settings for the SEO Analysis Tool"""
   
   def __init__(self):
       load_dotenv()
       
       # API Credentials
       self.GSC_CREDENTIALS = {
           'client_id': os.getenv('GSC_CLIENT_ID'),
           'client_secret': os.getenv('GSC_CLIENT_SECRET'),
           'redirect_uri': os.getenv('GSC_REDIRECT_URI')
       }
       
       # Moz API Token
       self.MOZ_TOKEN = os.getenv('MOZ_TOKEN')
       
       # API Rate Limits
       self.RATE_LIMITS = {
           'gsc': {'calls': 25000, 'period': 'day'},
           'moz': {'calls': 25, 'period': 'day'},
           'scraper': {'calls': 60, 'period': 'minute'}
       }
       
       # Cache Settings
       self.CACHE_DURATION = 24  # hours
       
       # Report Settings
       self.COST_RATES = {
           'basic': {'min': 40, 'max': 50},
           'standard': {'min': 50, 'max': 60}
       }

       # Scraper Settings
       self.SCRAPER_SETTINGS = {
           'timeout': 30,
           'user_agent': 'SEOAnalysisTool/1.0',
           'max_retries': 3,
           'retry_delay': 5
       }
       
       # Report Export Settings
       self.EXPORT_SETTINGS = {
           'pdf_page_size': 'A4',
           'default_language': 'nl',
           'company_name': 'SEO Analysis Tool'
       }

   def validate_credentials(self) -> Dict[str, bool]:
       """Validate API credentials"""
       return {
           'gsc': all(self.GSC_CREDENTIALS.values()),
           'moz': bool(self.MOZ_TOKEN)
       }
       
   def get_api_settings(self) -> Dict[str, Any]:
       """Get API configuration"""
       return {
           'rate_limits': self.RATE_LIMITS,
           'cache_duration': self.CACHE_DURATION,
           'scraper': self.SCRAPER_SETTINGS
       }
   
   def get_report_settings(self) -> Dict[str, Any]:
       """Get report configuration"""
       return {
           'cost_rates': self.COST_RATES,
           'export': self.EXPORT_SETTINGS
       }

   def update_rate_limits(self, new_limits: Dict[str, Dict]):
       """Update API rate limits"""
       self.RATE_LIMITS.update(new_limits)