from typing import Dict, Any, Optional
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import asyncio

class GSCClient:
    def __init__(self, credentials: Dict[str, Any], rate_limiter):
        self.credentials = Credentials.from_authorized_user_info(credentials)
        self.service = build('searchconsole', 'v1', credentials=self.credentials)
        self.rate_limiter = rate_limiter

    async def get_search_analytics(self, site_url: str, days: int = 30) -> Dict[str, Any]:
        """Get search analytics data from Google Search Console"""
        await self.rate_limiter.wait_if_needed('gsc')
        
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        try:
            response = self.service.searchanalytics().query(
                siteUrl=site_url,
                body={
                    'startDate': start_date.isoformat(),
                    'endDate': end_date.isoformat(),
                    'dimensions': ['query', 'page'],
                    'rowLimit': 1000
                }
            ).execute()
            
            return self._process_analytics_response(response)
        except Exception as e:
            return {'error': str(e)}

    def _process_analytics_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process and structure the GSC response data"""
        if 'rows' not in response:
            return {'clicks': 0, 'impressions': 0, 'ctr': 0, 'position': 0}
            
        total_clicks = sum(row['clicks'] for row in response['rows'])
        total_impressions = sum(row['impressions'] for row in response['rows'])
        
        return {
            'clicks': total_clicks,
            'impressions': total_impressions,
            'ctr': (total_clicks / total_impressions * 100) if total_impressions > 0 else 0,
            'position': sum(row['position'] for row in response['rows']) / len(response['rows'])
        }

    async def get_sitemaps(self, site_url: str) -> Dict[str, Any]:
        """Get sitemap information from GSC"""
        await self.rate_limiter.wait_if_needed('gsc')
        
        try:
            sitemaps = self.service.sitemaps().list(siteUrl=site_url).execute()
            return sitemaps
        except Exception as e:
            return {'error': str(e)}