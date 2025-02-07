from typing import Dict, Any, List
from ..rag.processor import RAGProcessor
from ..llm.analyzer import LLMAnalyzer


class AIInsightsGenerator:
    """Generates enhanced SEO insights by combining RAG and LLM outputs."""
    
    def __init__(self):
        self.rag_processor = RAGProcessor()
        self.llm_analyzer = LLMAnalyzer()

    async def generate_insights(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive insights."""
        try:
            print("🟢 Starting AI Insights Generation...")

            # Get insights from both systems
            rag_insights = await self.rag_processor.process(data)
            print(f"🔹 RAG Insights: {rag_insights}")

            llm_insights = await self.llm_analyzer.analyze(data)
            print(f"🔹 LLM Insights: {llm_insights}")

            # Combine and enhance insights
            combined_insights = await self._combine_insights(data, rag_insights, llm_insights)

            # Ensure priority actions exist
            if not combined_insights.get("priority_actions"):
                combined_insights["priority_actions"] = self._generate_basic_priority_actions(data)

            print(f"✅ AI Insights Generated: {combined_insights}")
            return combined_insights
        
        except Exception as e:
            print(f"❌ AI Insights Generation Error: {e}")
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
        """Combine and prioritize insights from both RAG and LLM."""
        return {
            'technical_insights': self._merge_insights(
                rag_insights.get('technical_insights', []),
                llm_insights.get('technical_insights', [])
            ),
            'content_insights': self._merge_insights(
                rag_insights.get('content_insights', []),
                llm_insights.get('content_insights', [])
            ),
            'strategic_recommendations': self._merge_insights(
                rag_insights.get('similar_cases', []),
                llm_insights.get('strategy_recommendations', [])
            ),
            'priority_actions': self._generate_priority_actions(data, rag_insights, llm_insights)
        }

    def _merge_insights(
        self, 
        rag_insights: List[Dict], 
        llm_insights: List[Dict]
    ) -> List[Dict]:
        """Merge and deduplicate insights."""
        merged = []
        seen_recommendations = set()

        for insight in rag_insights + llm_insights:
            key = f"{insight.get('metric', '')}_{insight.get('recommendation', '')}"
            if key not in seen_recommendations:
                merged.append({
                    **insight,
                    'confidence': self._calculate_confidence(insight)
                })
                seen_recommendations.add(key)

        return sorted(merged, key=lambda x: x['confidence'], reverse=True)

    def _generate_priority_actions(
        self,
        data: Dict[str, Any],
        rag_insights: Dict[str, Any],
        llm_insights: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate prioritized action items."""
        all_insights = []
        
        # Collect all insights
        all_insights.extend(self._get_priority_insights(rag_insights))
        all_insights.extend(self._get_priority_insights(llm_insights))

        if not all_insights:
            return self._generate_basic_priority_actions(data)

        # Sort and prioritize
        return sorted(
            all_insights,
            key=lambda x: (x.get('impact', 0) * x.get('confidence', 0)),
            reverse=True
        )[:5]  # Top 5 priority actions

    def _get_priority_insights(self, insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract priority insights from a set of insights."""
        priority_insights = []
        
        for category in ['technical_insights', 'content_insights']:
            for insight in insights.get(category, []):
                if insight.get('impact', 0) > 0.7:
                    priority_insights.append(insight)

        return priority_insights

    def _calculate_confidence(self, insight: Dict[str, Any]) -> float:
        """Calculate confidence score for an insight."""
        base_confidence = insight.get('confidence', 0.5)
        impact = insight.get('impact', 0.5)
        evidence = 1 if insight.get('evidence') else 0.6
        
        return (base_confidence + impact + evidence) / 3

    def _generate_basic_insights(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate basic insights when AI processing fails."""
        return {
            'technical_insights': self._basic_technical_insights(data),
            'content_insights': self._basic_content_insights(data),
            'priority_actions': self._generate_basic_priority_actions(data)
        }

    def _basic_technical_insights(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate basic technical insights without AI processing."""
        insights = []
        
        meta_tags = data.get('scraped_data', {}).get('meta_tags', {})
        if not meta_tags.get('meta_description'):
            insights.append({
                'type': 'technical',
                'metric': 'meta_description',
                'recommendation': 'Add meta description tag',
                'priority': 'high',
                'impact': 0.8
            })
        
        return insights

    def _basic_content_insights(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate basic content insights without AI processing."""
        insights = []
        
        content_data = data.get('scraped_data', {}).get('content', {})
        word_count = content_data.get('word_count', 0)
        if word_count < 300:
            insights.append({
                'type': 'content',
                'metric': 'word_count',
                'recommendation': 'Increase content length to at least 300 words',
                'priority': 'high',
                'impact': 0.7
            })
            
        return insights

    def _generate_basic_priority_actions(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate basic priority actions without AI processing."""
        actions = []
        
        all_insights = self._basic_technical_insights(data) + self._basic_content_insights(data)
        
        return sorted(
            all_insights,
            key=lambda x: x.get('impact', 0),
            reverse=True
        )[:3]  # Top 3 priority actions
