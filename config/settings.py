# config/settings.py
from typing import Dict, Any
import os
from dotenv import load_dotenv

class Settings:
   """Configuration settings for the SEO Analysis Tool"""
   
   def __init__(self):
       load_dotenv()  # Load environment variables
       
       # API Credentials
       self.GSC_CREDENTIALS = {
           'client_id': os.getenv('GSC_CLIENT_ID'),
           'client_secret': os.getenv('GSC_CLIENT_SECRET'),
           'redirect_uri': os.getenv('GSC_REDIRECT_URI')
       }
       
       self.MOZ_CREDENTIALS = {
           'access_id': os.getenv('MOZ_ACCESS_ID'),
           'secret_key': os.getenv('MOZ_SECRET_KEY')
       }
       
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
       
   def validate_credentials(self) -> Dict[str, bool]:
       """Validate API credentials"""
       return {
           'gsc': all(self.GSC_CREDENTIALS.values()),
           'moz': all(self.MOZ_CREDENTIALS.values())
       }
       
   def get_api_settings(self) -> Dict[str, Any]:
       """Get API configuration"""
       return {
           'rate_limits': self.RATE_LIMITS,
           'cache_duration': self.CACHE_DURATION
       }