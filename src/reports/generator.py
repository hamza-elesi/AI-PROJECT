from typing import Dict, Any, List
from .translations import DutchTranslator
import pandas as pd
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.translator = DutchTranslator()

    def generate_report(self, aggregated_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete SEO report"""
        try:
            return {
                'metadata': self._generate_metadata(),
                'overview': self._generate_overview(aggregated_data),
                'technical_analysis': self._generate_technical_analysis(aggregated_data),
                'recommendations': self._generate_recommendations(aggregated_data),
                'performance_metrics': self._generate_performance_metrics(aggregated_data)
            }
        except Exception as e:
            return {'error': str(e)}

    def _generate_metadata(self) -> Dict[str, str]:
        """Generate report metadata"""
        return {
            'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'report_type': self.translator.translate('seo_analysis'),
            'version': '1.0'
        }

    def _generate_overview(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overview section"""
        overview = data.get('overview', {})
        return {
            self.translator.translate('seo_score'): data.get('seo_score', 0),
            self.translator.translate('visibility'): overview.get('visibility', {}),
            self.translator.translate('authority'): overview.get('authority', {})
        }

    def _generate_technical_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate technical analysis section"""
        technical = data.get('technical_seo', {})
        return {
            'meta_tags': self._format_meta_tags(technical.get('meta_tags_status', {})),
            'technical_elements': self._format_technical_elements(technical.get('technical_elements', {}))
        }

    def _generate_recommendations(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations with time and cost estimates"""
        issues = self._identify_issues(data)
        return [
            {
                'issue': self.translator.translate(issue['type']),
                'priority': self.translator.translate(issue['priority']),
                'estimated_time': f"{issue['time']} {self.translator.translate('hours')}",
                'estimated_cost': f"€{issue['cost_min']}-{issue['cost_max']}",
                'steps': issue['steps']
            }
            for issue in issues
        ]

    def _generate_performance_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate performance metrics section"""
        performance = data.get('performance', {})
        return {
            self.translator.translate('search_visibility'): {
                self.translator.translate('clicks'): performance.get('clicks', 0),
                self.translator.translate('impressions'): performance.get('impressions', 0),
                self.translator.translate('ctr'): f"{performance.get('ctr', 0)}%",
                self.translator.translate('position'): performance.get('average_position', 0)
            },
            self.translator.translate('backlinks'): data.get('backlinks', {})
        }

    def _identify_issues(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify issues and create recommendations"""
        issues = []
        technical = data.get('technical_seo', {})
        content = data.get('content_analysis', {})

        # Check meta tags
        if not technical.get('meta_tags_status', {}).get('has_description'):
            issues.append({
                'type': 'missing_meta_description',
                'priority': 'high',
                'time': '2-3',
                'cost_min': 100,
                'cost_max': 150,
                'steps': [
                    self.translator.translate('review_missing_meta'),
                    self.translator.translate('create_meta_descriptions'),
                    self.translator.translate('implement_changes')
                ]
            })

        # Add more issue identification logic...
        return issues

    def generate_pdf(self, report_data: Dict[str, Any]) -> bytes:
        """Generate PDF report"""
        # PDF generation logic would go here
        # For Phase 1A, this could be a simple template
        pass

    def generate_html(self, report_data: Dict[str, Any]) -> str:
        """Generate HTML report"""
        # HTML generation logic would go here
        # For Phase 1A, this could be a simple template
        pass