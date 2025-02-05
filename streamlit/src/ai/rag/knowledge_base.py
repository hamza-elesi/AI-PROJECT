# src/ai/rag/knowledge_base.py

from typing import Dict, Any, List
import json
import os
from pathlib import Path

class SEOKnowledgeBase:
    """Manages SEO knowledge and guidelines"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent / 'knowledge'
        self.knowledge = self.load_knowledge()

    def load_knowledge(self) -> Dict[str, Any]:
        """Load all SEO knowledge from JSON files"""
        knowledge = {}
        
        # Load technical SEO guidelines
        knowledge['technical'] = self._load_category('technical_seo')
        
        # Load content guidelines
        knowledge['content'] = self._load_category('content_seo')
        
        # Load backlink guidelines
        knowledge['backlinks'] = self._load_category('backlink_analysis')
        
        return knowledge

    def _load_category(self, category: str) -> Dict[str, Any]:
        """Load knowledge for a specific category"""
        category_path = self.base_path / category
        category_data = {}
        
        if category_path.exists():
            for file_path in category_path.glob('*.json'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    category_data[file_path.stem] = json.load(f)
        
        return category_data

    def get_guidelines(self, category: str, aspect: str) -> Dict[str, Any]:
        """Get specific guidelines from the knowledge base"""
        return self.knowledge.get(category, {}).get(aspect, {})

    def get_recommendations(self, category: str, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get recommendations based on metrics"""
        guidelines = self.get_guidelines(category, 'recommendations')
        recommendations = []
        
        for metric, value in metrics.items():
            if metric in guidelines:
                recommendations.extend(self._evaluate_metric(
                    metric, 
                    value, 
                    guidelines[metric]
                ))
                
        return recommendations

    def _evaluate_metric(self, metric: str, value: Any, guidelines: Dict) -> List[Dict[str, Any]]:
        """Evaluate a metric against guidelines"""
        recommendations = []
        
        thresholds = guidelines.get('thresholds', {})
        for level, threshold in thresholds.items():
            if self._meets_threshold(value, threshold):
                recommendations.append({
                    'metric': metric,
                    'level': level,
                    'recommendation': guidelines['recommendations'][level],
                    'current_value': value,
                    'target_value': threshold
                })
                
        return recommendations

    def _meets_threshold(self, value: Any, threshold: Any) -> bool:
        """Check if value meets a threshold condition"""
        if isinstance(threshold, dict):
            operator = threshold.get('operator', '>')
            threshold_value = threshold.get('value')
            
            if operator == '>':
                return value > threshold_value
            elif operator == '<':
                return value < threshold_value
            elif operator == '>=':
                return value >= threshold_value
            elif operator == '<=':
                return value <= threshold_value
            
        return value == threshold