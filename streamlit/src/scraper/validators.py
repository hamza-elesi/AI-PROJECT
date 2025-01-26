from urllib.parse import urlparse
import requests
from typing import Dict, Any, Optional
from urllib.robotparser import RobotFileParser

class URLValidator:
    def __init__(self):
        self.robot_parser = RobotFileParser()

    def is_valid_url(self, url: str) -> bool:
        """Validate URL format and accessibility"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def check_robots_txt(self, url: str) -> Dict[str, Any]:
        """Check robots.txt rules and availability"""
        try:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            robots_url = f"{base_url}/robots.txt"
            
            self.robot_parser.set_url(robots_url)
            self.robot_parser.read()
            
            can_crawl = self.robot_parser.can_fetch("*", url)
            
            return {
                'has_robots_txt': True,
                'can_crawl': can_crawl,
                'robots_url': robots_url
            }
        except Exception as e:
            return {
                'has_robots_txt': False,
                'can_crawl': True,  # Default to True if no robots.txt
                'error': str(e)
            }

    def validate_response(self, response: requests.Response) -> Dict[str, Any]:
        """Validate HTTP response"""
        return {
            'status_code': response.status_code,
            'is_success': 200 <= response.status_code < 300,
            'content_type': response.headers.get('content-type', ''),
            'response_time': response.elapsed.total_seconds()
        }