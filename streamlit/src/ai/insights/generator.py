# src/ai/insights/generator.py

from typing import Dict, Any, List
from ..rag.processor import RAGProcessor
from ..llm.analyzer import LLMAnalyzer

class AIInsightsGenerator:
    """Generates enhanced SEO insights by combining RAG and LLM outputs"""
    
    def __init__(self):
        self.rag_processor = RAGProcessor()
        self.llm_analyzer = LLMAnalyzer()

    async def generate_insights(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive insights"""
        try:
            # Get insights from both systems
            rag_insights = await self.rag_processor.process(data)
            llm_insights = await self.llm_analyzer.analyze(data)
            
            # Combine and enhance insights
            return await self._combine_insights(data, rag_insights, llm_insights)
        except Exception as e:
            return {
                'error': str(e),
                'basic_insights': self._generate_basic_insights(data)
            }

    async def _combine_insights(
        self, 
        data: Dict[str, Any],
        rag_insights: Dict[str, Any],
        llm_insights: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Combine and prioritize insights from both systems"""
        return {
            'technical_insights': self._merge_technical_insights(
                rag_insights.get('technical_insights', []),
                llm_insights.get('technical_insights', [])
            ),
            'content_insights': self._merge_content_insights(
                rag_insights.get('content_insights', []),
                llm_insights.get('content_insights', [])
            ),
            'strategic_recommendations': self._merge_strategic_insights(
                rag_insights.get('similar_cases', []),
                llm_insights.get('strategy_recommendations', [])
            ),
            'priority_actions': self._generate_priority_actions(
                data, rag_insights, llm_insights
            )
        }

    def _merge_technical_insights(
        self, 
        rag_insights: List[Dict], 
        llm_insights: List[Dict]
    ) -> List[Dict]:
        """Merge and deduplicate technical insights"""
        merged = []
        seen_recommendations = set()

        # Process RAG insights
        for insight in rag_insights:
            key = f"{insight.get('metric')}_{insight.get('recommendation')}"
            if key not in seen_recommendations:
                merged.append({
                    **insight,
                    'source': 'rag',
                    'confidence': self._calculate_confidence(insight)
                })
                seen_recommendations.add(key)

        # Process LLM insights
        for insight in llm_insights:
            key = f"{insight.get('metric')}_{insight.get('recommendation')}"
            if key not in seen_recommendations:
                merged.append({
                    **insight,
                    'source': 'llm',
                    'confidence': self._calculate_confidence(insight)
                })
                seen_recommendations.add(key)

        return sorted(merged, key=lambda x: x['confidence'], reverse=True)

    def _merge_content_insights(
        self, 
        rag_insights: List[Dict], 
        llm_insights: List[Dict]
    ) -> List[Dict]:
        """Merge and enhance content insights"""
        merged = []
        seen_aspects = set()

        for insight in rag_insights + llm_insights:
            aspect = insight.get('aspect')
            if aspect not in seen_aspects:
                enhanced_insight = self._enhance_content_insight(insight)
                if enhanced_insight:
                    merged.append(enhanced_insight)
                    seen_aspects.add(aspect)

        return sorted(merged, key=lambda x: x.get('impact_score', 0), reverse=True)

    def _merge_strategic_insights(
        self, 
        similar_cases: List[Dict], 
        llm_recommendations: List[Dict]
    ) -> List[Dict]:
        """Generate strategic insights based on similar cases and LLM recommendations"""
        strategic_insights = []
        
        # Process similar cases
        for case in similar_cases:
            if case.get('similarity_score', 0) > 0.8:
                strategic_insights.append({
                    'type': 'case_based',
                    'recommendation': case.get('content'),
                    'confidence': case.get('similarity_score'),
                    'source': 'similar_case'
                })

        # Process LLM recommendations
        for rec in llm_recommendations:
            strategic_insights.append({
                'type': 'ai_generated',
                'recommendation': rec.get('recommendation'),
                'confidence': rec.get('confidence', 0.7),
                'source': 'llm'
            })

        return sorted(strategic_insights, key=lambda x: x['confidence'], reverse=True)

    def _generate_priority_actions(
        self,
        data: Dict[str, Any],
        rag_insights: Dict[str, Any],
        llm_insights: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate prioritized action items"""
        all_insights = []
        
        # Collect all insights
        all_insights.extend(self._get_priority_insights(rag_insights))
        all_insights.extend(self._get_priority_insights(llm_insights))

        # Sort and prioritize
        return sorted(
            all_insights,
            key=lambda x: (x.get('impact', 0) * x.get('confidence', 0)),
            reverse=True
        )[:5]  # Top 5 priority actions

    def _get_priority_insights(self, insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract priority insights from a set of insights"""
        priority_insights = []
        
        for category in ['technical_insights', 'content_insights']:
            for insight in insights.get(category, []):
                if insight.get('impact', 0) > 0.7:
                    priority_insights.append(insight)

        return priority_insights

    def _calculate_confidence(self, insight: Dict[str, Any]) -> float:
        """Calculate confidence score for an insight"""
        base_confidence = insight.get('confidence', 0.5)
        impact = insight.get('impact', 0.5)
        evidence = 1 if insight.get('evidence') else 0.6
        
        return (base_confidence + impact + evidence) / 3

    def _enhance_content_insight(self, insight: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance content insight with additional context"""
        if not insight:
            return None

        return {
            **insight,
            'impact_score': self._calculate_impact_score(insight),
            'implementation_difficulty': self._estimate_difficulty(insight),
            'expected_benefits': self._estimate_benefits(insight)
        }

    def _calculate_impact_score(self, insight: Dict[str, Any]) -> float:
        """Calculate impact score for an insight"""
        base_impact = insight.get('impact', 0.5)
        urgency = insight.get('urgency', 0.5)
        importance = insight.get('importance', 0.5)
        
        return (base_impact + urgency + importance) / 3

    def _estimate_difficulty(self, insight: Dict[str, Any]) -> str:
        """Estimate implementation difficulty"""
        if 'technical' in insight.get('type', '').lower():
            return 'High'
        elif 'content' in insight.get('type', '').lower():
            return 'Medium'
        return 'Low'

    def _estimate_benefits(self, insight: Dict[str, Any]) -> List[str]:
        """Estimate expected benefits"""
        benefits = []
        if insight.get('impact_score', 0) > 0.7:
            benefits.append('Significant SEO improvement')
        if insight.get('type') == 'technical':
            benefits.append('Better search engine crawling')
        if insight.get('type') == 'content':
            benefits.append('Improved user engagement')
        return benefits

    def _generate_basic_insights(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate basic insights when AI processing fails"""
        return {
            'technical_insights': self._basic_technical_insights(data),
            'content_insights': self._basic_content_insights(data),
            'priority_actions': self._basic_priority_actions(data)
        }