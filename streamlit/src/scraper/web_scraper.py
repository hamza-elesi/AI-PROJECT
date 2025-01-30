from urllib.parse import urlparse
from bs4 import BeautifulSoup
import aiohttp
from typing import Dict, Any
from .validators import URLValidator


class SEOScraper:
    def __init__(self):
        self.validator = URLValidator()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; SEOAnalysisTool/1.0)'
        }

    async def scrape_page(self, url: str) -> Dict[str, Any]:
        """Main scraping function"""
        if not self.validator.is_valid_url(url):
            return {'error': 'Invalid URL format'}

        robots_check = self.validator.check_robots_txt(url)
        if not robots_check['can_crawl']:
            return {'error': 'Crawling not allowed by robots.txt'}

        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(url) as response:
                    html = await response.text()
                    validation = self.validator.validate_response(response)

                    if not validation['is_success']:
                        return {'error': f"HTTP {validation['status_code']}"}

                    return await self.analyze_content(html, url)
        except Exception as e:
            return {'error': str(e)}

    async def analyze_content(self, html: str, url: str) -> Dict[str, Any]:
        """Analyze page content for SEO elements"""
        soup = BeautifulSoup(html, 'html.parser')

        return {
            'meta_tags': self._analyze_meta_tags(soup),
            'headings': self._analyze_headings(soup),
            'images': self._analyze_images(soup),
            'links': self._analyze_links(soup, url),
            'content': self._analyze_content_quality(soup),
            'technical': self._analyze_technical_elements(soup)
        }

    def _analyze_meta_tags(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze meta tags"""
        return {
            'title': soup.title.string if soup.title else None,
            'meta_description': soup.find('meta', {'name': 'description'}).get('content', None) if soup.find('meta', {'name': 'description'}) else None,
            'meta_keywords': soup.find('meta', {'name': 'keywords'}).get('content', None) if soup.find('meta', {'name': 'keywords'}) else None,
            'viewport': soup.find('meta', {'name': 'viewport'}).get('content', None) if soup.find('meta', {'name': 'viewport'}) else None,
            'charset': soup.find('meta', {'charset': True}).get('charset', None) if soup.find('meta', {'charset': True}) else None
        }

    def _analyze_headings(self, soup: BeautifulSoup) -> Dict[str, int]:
        """Analyze heading structure"""
        return {f'h{i}': len(soup.find_all(f'h{i}')) for i in range(1, 7)}

    def _analyze_images(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze image optimization"""
        images = soup.find_all('img')
        return {
            'total_images': len(images),
            'missing_alt': len([img for img in images if not img.get('alt')]),
            'missing_src': len([img for img in images if not img.get('src')]),
        }

    def _analyze_links(self, soup: BeautifulSoup, base_url: str) -> Dict[str, Any]:
        """Analyze internal and external links"""
        links = soup.find_all('a')
        parsed_base = urlparse(base_url)

        internal_links = []
        external_links = []

        for link in links:
            href = link.get('href')
            if href:
                if href.startswith('/') or parsed_base.netloc in href:
                    internal_links.append(href)
                else:
                    external_links.append(href)

        return {
            'internal_links': len(internal_links),
            'external_links': len(external_links),
            'total_links': len(links)
        }

    def _analyze_content_quality(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Basic content quality analysis"""
        text = soup.get_text()
        words = text.split()

        return {
            'word_count': len(words),
            'paragraphs': len(soup.find_all('p')),
            'has_structured_data': bool(soup.find_all('script', {'type': 'application/ld+json'}))
        }

    def _analyze_technical_elements(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze technical SEO elements"""
        return {
            'has_canonical': bool(soup.find('link', {'rel': 'canonical'})),
            'has_favicon': bool(soup.find('link', {'rel': ['icon', 'shortcut icon']})),
            'has_viewport': bool(soup.find('meta', {'name': 'viewport'}))
        }

