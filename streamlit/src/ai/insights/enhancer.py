# src/ai/insights/enhancer.py

from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class InsightMetadata:
    """Metadata for enhanced insights"""
    confidence: float
    impact: float
    priority: str
    implementation_time: str
    estimated_cost: str
    timestamp: datetime

class InsightsEnhancer:
    """Enhances and refines AI-generated insights"""
    
    def __init__(self):
        self.priority_levels = ['Critical', 'High', 'Medium', 'Low']
        self.implementation_times = {
            'quick': '< 1 hour',
            'medium': '2-4 hours',
            'long': '4+ hours'
        }

    async def enhance_insights(self, insights: Dict[str, Any]) -> Dict[str, Any]:
        """Main method to enhance insights"""
        try:
            enhanced = {
                'technical': self._enhance_technical_insights(
                    insights.get('technical_insights', [])
                ),
                'content': self._enhance_content_insights(
                    insights.get('content_insights', [])
                ),
                'strategic': self._enhance_strategic_insights(
                    insights.get('strategic_recommendations', [])
                ),
                'priorities': self._enhance_priority_actions(
                    insights.get('priority_actions', [])
                )
            }

            # Add summary and metadata
            enhanced['summary'] = self._generate_summary(enhanced)
            enhanced['metadata'] = self._generate_metadata(enhanced)
            
            return enhanced
        
        except Exception as e:
            return {
                'error': f'Enhancement failed: {str(e)}',
                'original_insights': insights
            }

    def _enhance_technical_insights(
        self, 
        technical_insights: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Enhance technical SEO insights"""
        enhanced = []
        
        for insight in technical_insights:
            enhanced_insight = {
                **insight,
                'metadata': InsightMetadata(
                    confidence=self._calculate_confidence(insight),
                    impact=self._calculate_impact(insight),
                    priority=self._determine_priority(insight),
                    implementation_time=self._estimate_implementation_time(insight),
                    estimated_cost=self._estimate_cost(insight),
                    timestamp=datetime.now()
                )
            }
            
            # Add implementation steps
            enhanced_insight['implementation_steps'] = self._generate_implementation_steps(
                insight
            )
            
            enhanced.append(enhanced_insight)
        
        return sorted(enhanced, key=lambda x: x['metadata'].impact, reverse=True)

    def _enhance_content_insights(
        self, 
        content_insights: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Enhance content-related insights"""
        enhanced = []
        
        for insight in content_insights:
            enhanced_insight = {
                **insight,
                'metadata': InsightMetadata(
                    confidence=self._calculate_confidence(insight),
                    impact=self._calculate_impact(insight),
                    priority=self._determine_priority(insight),
                    implementation_time=self._estimate_implementation_time(insight),
                    estimated_cost=self._estimate_cost(insight),
                    timestamp=datetime.now()
                )
            }
            
            # Add content-specific enhancements
            enhanced_insight.update({
                'readability_impact': self._assess_readability_impact(insight),
                'seo_impact': self._assess_seo_impact(insight),
                'user_experience_impact': self._assess_user_experience_impact(insight)
            })
            
            enhanced.append(enhanced_insight)
        
        return sorted(enhanced, key=lambda x: x['metadata'].impact, reverse=True)

    def _enhance_strategic_insights(
        self, 
        strategic_insights: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Enhance strategic recommendations"""
        enhanced = []
        
        for insight in strategic_insights:
            enhanced_insight = {
                **insight,
                'metadata': InsightMetadata(
                    confidence=self._calculate_confidence(insight),
                    impact=self._calculate_impact(insight),
                    priority=self._determine_priority(insight),
                    implementation_time=self._estimate_implementation_time(insight),
                    estimated_cost=self._estimate_cost(insight),
                    timestamp=datetime.now()
                )
            }
            
            # Add strategic-specific enhancements
            enhanced_insight.update({
                'long_term_impact': self._assess_long_term_impact(insight),
                'resource_requirements': self._assess_resource_requirements(insight),
                'competitive_advantage': self._assess_competitive_advantage(insight)
            })
            
            enhanced.append(enhanced_insight)
        
        return sorted(enhanced, key=lambda x: x['metadata'].impact, reverse=True)

    def _enhance_priority_actions(
        self, 
        priority_actions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Enhance priority actions"""
        enhanced = []
        
        for action in priority_actions:
            enhanced_action = {
                **action,
                'metadata': InsightMetadata(
                    confidence=self._calculate_confidence(action),
                    impact=self._calculate_impact(action),
                    priority=self._determine_priority(action),
                    implementation_time=self._estimate_implementation_time(action),
                    estimated_cost=self._estimate_cost(action),
                    timestamp=datetime.now()
                )
            }
            
            # Add action-specific enhancements
            enhanced_action.update({
                'quick_wins': self._identify_quick_wins(action),
                'dependencies': self._identify_dependencies(action),
                'success_metrics': self._define_success_metrics(action)
            })
            
            enhanced.append(enhanced_action)
        
        return sorted(enhanced, key=lambda x: x['metadata'].impact, reverse=True)[:5]

    def _calculate_confidence(self, insight: Dict[str, Any]) -> float:
        """Calculate confidence score"""
        base_confidence = insight.get('confidence', 0.5)
        source_reliability = 0.9 if insight.get('source') == 'rag' else 0.7
        evidence_strength = 0.8 if insight.get('evidence') else 0.5
        
        return (base_confidence + source_reliability + evidence_strength) / 3

    def _calculate_impact(self, insight: Dict[str, Any]) -> float:
        """Calculate impact score"""
        base_impact = insight.get('impact', 0.5)
        urgency = insight.get('urgency', 0.5)
        scope = insight.get('scope', 0.5)
        
        return (base_impact + urgency + scope) / 3

    def _determine_priority(self, insight: Dict[str, Any]) -> str:
        """Determine priority level"""
        impact = self._calculate_impact(insight)
        confidence = self._calculate_confidence(insight)
        
        combined_score = (impact + confidence) / 2
        
        if combined_score > 0.8:
            return 'Critical'
        elif combined_score > 0.6:
            return 'High'
        elif combined_score > 0.4:
            return 'Medium'
        return 'Low'

    def _estimate_implementation_time(self, insight: Dict[str, Any]) -> str:
        """Estimate implementation time"""
        if insight.get('type') == 'technical':
            return self.implementation_times['medium']
        elif insight.get('type') == 'content':
            return self.implementation_times['long']
        return self.implementation_times['quick']

    def _estimate_cost(self, insight: Dict[str, Any]) -> str:
        """Estimate implementation cost"""
        base_cost = {
            'technical': '$100-200',
            'content': '$150-300',
            'strategic': '$200-400'
        }
        return base_cost.get(insight.get('type', 'technical'), '$100-200')

    def _generate_implementation_steps(self, insight: Dict[str, Any]) -> List[str]:
        """Generate implementation steps"""
        return [
            f"1. {insight.get('action', 'Implement change')}",
            "2. Test implementation",
            "3. Monitor results",
            "4. Adjust if needed"
        ]

    def _generate_summary(self, enhanced_insights: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall summary"""
        return {
            'total_insights': len(enhanced_insights.get('technical', [])) + 
                            len(enhanced_insights.get('content', [])) +
                            len(enhanced_insights.get('strategic', [])),
            'critical_issues': len([i for i in enhanced_insights.get('priorities', [])
                                if i['metadata'].priority == 'Critical']),
            'quick_wins': len([i for i in enhanced_insights.get('priorities', [])
                             if i['metadata'].implementation_time == self.implementation_times['quick']]),
            'estimated_total_cost': self._calculate_total_cost(enhanced_insights)
        }

    def _generate_metadata(self, enhanced_insights: Dict[str, Any]) -> Dict[str, Any]:
        """Generate metadata for the entire analysis"""
        return {
            'timestamp': datetime.now(),
            'version': '1.0',
            'confidence_score': self._calculate_average_confidence(enhanced_insights),
            'completeness_score': self._calculate_completeness_score(enhanced_insights)
        }

    def _calculate_total_cost(self, insights: Dict[str, Any]) -> str:
        """Calculate total estimated cost"""
        total_min = 0
        total_max = 0
        
        for category in ['technical', 'content', 'strategic']:
            for insight in insights.get(category, []):
                cost_str = insight['metadata'].estimated_cost
                min_cost, max_cost = map(int, cost_str.replace('$', '').split('-'))
                total_min += min_cost
                total_max += max_cost
        
        return f"${total_min}-{total_max}"

    def _calculate_average_confidence(self, insights: Dict[str, Any]) -> float:
        """Calculate average confidence across all insights"""
        confidences = []
        for category in ['technical', 'content', 'strategic']:
            confidences.extend([i['metadata'].confidence for i in insights.get(category, [])])
        
        return sum(confidences) / len(confidences) if confidences else 0.0

    def _calculate_completeness_score(self, insights: Dict[str, Any]) -> float:
        """Calculate completeness score of the analysis"""
        expected_categories = {'technical', 'content', 'strategic', 'priorities'}
        actual_categories = set(insights.keys())
        
        return len(actual_categories.intersection(expected_categories)) / len(expected_categories)