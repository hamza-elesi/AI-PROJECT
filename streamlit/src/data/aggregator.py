from typing import Dict, Any, List


class DataAggregator:
    def __init__(self):
        self.score_weights = {
            'technical': 0.5,  # Increased weight since GSC data is removed
            'content': 0.3,
            'backlinks': 0.2  # Updated weights to balance only Moz and scraper
        }

    def aggregate_data(self, collected_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aggregate and structure all collected data.
        """
        try:
            moz_data = collected_data.get('moz_data', {})
            scraped_data = collected_data.get('scraped_data', {})

            return {
                'overview': self._calculate_overview(moz_data, scraped_data),
                'technical_seo': self._analyze_technical_seo(scraped_data),
                'content_analysis': self._analyze_content(scraped_data),
                'backlinks': self._analyze_backlinks(moz_data),
                'seo_score': self._calculate_seo_score(moz_data, scraped_data)
            }
        except Exception as e:
            return {'error': str(e)}

    def _calculate_overview(self, moz_data: Dict, scraped_data: Dict) -> Dict[str, Any]:
        """Calculate overview metrics."""
        return {
            'visibility': {
                'domain_authority': moz_data.get('metrics', {}).get('domain_authority', 0),
                'page_authority': moz_data.get('metrics', {}).get('page_authority', 0)
            },
            'content': {
                'word_count': scraped_data.get('content', {}).get('word_count', 0),
                'headings': scraped_data.get('headings', {})
            }
        }

    def _analyze_technical_seo(self, scraped_data: Dict) -> Dict[str, Any]:
        """Analyze technical SEO aspects."""
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
        """Analyze content quality."""
        content = scraped_data.get('content', {})
        return {
            'word_count': content.get('word_count', 0),
            'paragraphs': content.get('paragraphs', 0),
            'headings_structure': scraped_data.get('headings', {})
        }

    def _analyze_backlinks(self, moz_data: Dict) -> Dict[str, Any]:
        """Analyze backlink profile."""
        metrics = moz_data.get('metrics', {})
        return {
            'total_links': metrics.get('total_links', 0),
            'linking_domains': metrics.get('linking_domains', 0),
            'domain_authority': metrics.get('domain_authority', 0)
        }

    def _calculate_seo_score(self, moz_data: Dict, scraped_data: Dict) -> int:
        """Calculate overall SEO score."""
        try:
            # Technical score
            technical_score = self._calculate_technical_score(scraped_data)

            # Content score
            content_score = self._calculate_content_score(scraped_data)

            # Backlink score
            backlink_score = self._calculate_backlink_score(moz_data)

            # Weighted average
            final_score = (
                technical_score * self.score_weights['technical'] +
                content_score * self.score_weights['content'] +
                backlink_score * self.score_weights['backlinks']
            )

            return round(final_score)

        except Exception:
            return 0

    def _calculate_technical_score(self, scraped_data: Dict) -> float:
        """Calculate technical SEO score."""
        technical = scraped_data.get('technical', {})
        score = 0

        # Scoring logic
        if technical.get('has_canonical'):
            score += 30
        if technical.get('has_viewport'):
            score += 30
        if technical.get('has_favicon'):
            score += 20
        if scraped_data.get('meta_tags', {}).get('has_title'):
            score += 20

        return min(score, 100)  # Cap the score at 100

    def _calculate_content_score(self, scraped_data: Dict) -> float:
        """Calculate content quality score."""
        content = scraped_data.get('content', {})
        word_count = content.get('word_count', 0)

        # Basic scoring logic based on word count
        if word_count >= 1000:
            return 100
        elif word_count >= 500:
            return 70
        elif word_count >= 200:
            return 40
        else:
            return 20

    def _calculate_backlink_score(self, moz_data: Dict) -> float:
        """Calculate backlink profile score."""
        metrics = moz_data.get('metrics', {})
        domain_authority = metrics.get('domain_authority', 0)

        # Scale domain authority to 100
        return min(domain_authority, 100)


# Example Usage
if __name__ == "__main__":
    aggregator = DataAggregator()

    collected_data = {
        "moz_data": {
            "metrics": {
                "domain_authority": 80,
                "page_authority": 70,
                "total_links": 500,
                "linking_domains": 50
            }
        },
        "scraped_data": {
            "meta_tags": {
                "title": "Example Title",
                "meta_description": "Example description",
                "viewport": "width=device-width, initial-scale=1.0"
            },
            "content": {
                "word_count": 1200,
                "paragraphs": 15
            },
            "technical": {
                "has_canonical": True,
                "has_favicon": True,
                "has_viewport": True
            },
            "headings": {
                "h1": 2,
                "h2": 5,
                "h3": 8
            }
        }
    }

    aggregated_result = aggregator.aggregate_data(collected_data)
    print(aggregated_result)
