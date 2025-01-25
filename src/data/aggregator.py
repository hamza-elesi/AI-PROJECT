from typing import Dict, Any, List

class DataAggregator:
    def __init__(self):
        self.score_weights = {
            'technical': 0.3,
            'content': 0.3,
            'performance': 0.2,
            'backlinks': 0.2
        }

    def aggregate_data(self, collected_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aggregate and structure all collected data
        """
        try:
            gsc_data = collected_data.get('gsc_data', {})
            moz_data = collected_data.get('moz_data', {})
            scraped_data = collected_data.get('scraped_data', {})

            return {
                'overview': self._calculate_overview(gsc_data, moz_data, scraped_data),
                'technical_seo': self._analyze_technical_seo(scraped_data),
                'content_analysis': self._analyze_content(scraped_data),
                'performance': self._analyze_performance(gsc_data),
                'backlinks': self._analyze_backlinks(moz_data),
                'seo_score': self._calculate_seo_score(gsc_data, moz_data, scraped_data)
            }
        except Exception as e:
            return {'error': str(e)}

    def _calculate_overview(self, gsc_data: Dict, moz_data: Dict, scraped_data: Dict) -> Dict[str, Any]:
        """Calculate overview metrics"""
        return {
            'visibility': {
                'organic_clicks': gsc_data.get('analytics', {}).get('clicks', 0),
                'impressions': gsc_data.get('analytics', {}).get('impressions', 0),
                'average_position': gsc_data.get('analytics', {}).get('position', 0)
            },
            'authority': {
                'domain_authority': moz_data.get('metrics', {}).get('domain_authority', 0),
                'page_authority': moz_data.get('metrics', {}).get('page_authority', 0)
            }
        }

    def _analyze_technical_seo(self, scraped_data: Dict) -> Dict[str, Any]:
        """Analyze technical SEO aspects"""
        meta_tags = scraped_data.get('meta_tags', {})
        technical = scraped_data.get('technical', {})
        
        return {
            'meta_tags_status': {
                'has_title': bool(meta_tags.get('title')),
                'has_description': bool(meta_tags.get('meta_description')),
                'has_viewport': bool(meta_tags.get('viewport'))
            },
            'technical_elements': technical
        }

    def _analyze_content(self, scraped_data: Dict) -> Dict[str, Any]:
        """Analyze content quality"""
        content = scraped_data.get('content', {})
        return {
            'word_count': content.get('word_count', 0),
            'paragraphs': content.get('paragraphs', 0),
            'headings_structure': scraped_data.get('headings', {})
        }

    def _analyze_performance(self, gsc_data: Dict) -> Dict[str, Any]:
        """Analyze search performance"""
        analytics = gsc_data.get('analytics', {})
        return {
            'clicks': analytics.get('clicks', 0),
            'impressions': analytics.get('impressions', 0),
            'ctr': analytics.get('ctr', 0),
            'average_position': analytics.get('position', 0)
        }

    def _analyze_backlinks(self, moz_data: Dict) -> Dict[str, Any]:
        """Analyze backlink profile"""
        metrics = moz_data.get('metrics', {})
        return {
            'total_links': metrics.get('total_links', 0),
            'linking_domains': metrics.get('linking_domains', 0),
            'domain_authority': metrics.get('domain_authority', 0)
        }

    def _calculate_seo_score(self, gsc_data: Dict, moz_data: Dict, scraped_data: Dict) -> int:
        """Calculate overall SEO score"""
        try:
            # Technical score
            technical_score = self._calculate_technical_score(scraped_data)
            
            # Content score
            content_score = self._calculate_content_score(scraped_data)
            
            # Performance score
            performance_score = self._calculate_performance_score(gsc_data)
            
            # Backlink score
            backlink_score = self._calculate_backlink_score(moz_data)
            
            # Weighted average
            final_score = (
                technical_score * self.score_weights['technical'] +
                content_score * self.score_weights['content'] +
                performance_score * self.score_weights['performance'] +
                backlink_score * self.score_weights['backlinks']
            )
            
            return round(final_score)
            
        except Exception:
            return 0

    def _calculate_technical_score(self, scraped_data: Dict) -> float:
        # Implementation of technical scoring logic
        pass

    def _calculate_content_score(self, scraped_data: Dict) -> float:
        # Implementation of content scoring logic
        pass

    def _calculate_performance_score(self, gsc_data: Dict) -> float:
        # Implementation of performance scoring logic
        pass

    def _calculate_backlink_score(self, moz_data: Dict) -> float:
        # Implementation of backlink scoring logic
        pass