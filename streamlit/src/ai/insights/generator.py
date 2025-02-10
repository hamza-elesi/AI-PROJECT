from typing import Dict, Any, List, Union
import json
from ..rag.processor import RAGProcessor
from ..llm.analyzer import LLMAnalyzer

class AIInsightsGenerator:
    """Generates enhanced SEO insights by combining RAG and LLM outputs."""

    def __init__(self):
        self.rag_processor = RAGProcessor()
        self.llm_analyzer = LLMAnalyzer()

    async def generate_insights(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive insights from RAG & LLM."""
        try:
            print("🟢 Starting AI Insights Generation...")

            # Step 1: Get insights from RAG
            rag_insights = await self.rag_processor.process(data)
            print(f"🔹 RAG Insights Received: {rag_insights}")

            # Step 2: Get insights from LLM
            llm_insights_raw = await self.llm_analyzer.analyze(data)

            # Ensure LLM response is parsed correctly
            llm_insights = self._parse_llm_response(llm_insights_raw)
            print(f"🔹 LLM Insights Parsed: {llm_insights}")

            # Step 3: Combine and enhance insights
            combined_insights = await self._combine_insights(data, rag_insights, llm_insights)

            # Step 4: Ensure priority actions exist
            if not combined_insights.get("priority_actions"):
                combined_insights["priority_actions"] = self._generate_priority_actions(data, rag_insights, llm_insights)

            print(f"✅ Final AI Insights: {combined_insights}")
            return combined_insights

        except Exception as e:
            print(f"❌ AI Insights Generation Error: {e}")
            return {
                'error': str(e),
                'basic_insights': self._generate_basic_insights(data)
            }

    def _parse_llm_response(self, response: Any) -> Dict[str, Any]:
        """Ensure LLM response is correctly formatted."""
        if isinstance(response, str):
            try:
                parsed_response = json.loads(response)
                if isinstance(parsed_response, dict):
                    return parsed_response
                else:
                    print("⚠️ LLM response is not a dictionary, returning empty insights.")
            except json.JSONDecodeError as e:
                print(f"❌ JSON Parsing Error: {e}, returning empty insights.")
        elif isinstance(response, dict):
            return response  # Already correctly formatted
        return {}

    async def _combine_insights(
        self, 
        data: Dict[str, Any],
        rag_insights: Dict[str, Any],
        llm_insights: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Combine and prioritize insights from RAG and LLM."""
        return {
            'technical_insights': self._merge_insights(
                rag_insights.get('technical_insights', []),
                self._convert_to_list(llm_insights.get('technical_insights', []))
            ),
            'content_insights': self._merge_insights(
                rag_insights.get('content_insights', []),
                self._convert_to_list(llm_insights.get('content_insights', []))
            ),
            'backlink_insights': self._merge_insights(
                rag_insights.get('backlink_insights', []),
                self._convert_to_list(llm_insights.get('backlink_insights', []))
            ),
            'strategic_recommendations': self._merge_strategy_insights(
                rag_insights.get('similar_cases', []),
                self._convert_to_list(llm_insights.get('strategy_recommendations', []))
            ),
            'priority_actions': self._generate_priority_actions(data, rag_insights, llm_insights)
        }

    def _merge_insights(self, rag_insights: List[Dict], llm_insights: List[Dict]) -> List[Dict]:
        """Merge and deduplicate insights."""
        merged = []
        seen_recommendations = set()

        for insight in rag_insights + llm_insights:
            if isinstance(insight, dict):
                key = f"{insight.get('metric', '')}_{insight.get('recommendation', '')}"
                if key not in seen_recommendations:
                    merged.append({
                        **insight,
                        'confidence': self._calculate_confidence(insight)
                    })
                    seen_recommendations.add(key)

        return sorted(merged, key=lambda x: x.get('confidence', 0), reverse=True)

    def _merge_strategy_insights(self, similar_cases: List[Dict], llm_recommendations: List[Dict]) -> List[Dict]:
        """Generate strategic insights based on similar cases and LLM recommendations."""
        strategic_insights = []

        for case in similar_cases:
            if isinstance(case, dict) and case.get('similarity_score', 0) > 0.5:
                strategic_insights.append({
                    'type': 'case_based',
                    'recommendation': case.get('content'),
                    'confidence': case.get('similarity_score'),
                    'source': 'similar_case'
                })

        for rec in llm_recommendations:
            if isinstance(rec, dict):
                strategic_insights.append({
                    'type': 'ai_generated',
                    'recommendation': rec.get('recommendation', 'No Recommendation'),
                    'confidence': 0.7,
                    'source': 'llm'
                })

        return sorted(strategic_insights, key=lambda x: x['confidence'], reverse=True)

    def _generate_priority_actions(self, data: Dict[str, Any], rag_insights: Dict[str, Any], llm_insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate prioritized action items."""
        all_insights = self._get_priority_insights(rag_insights) + self._get_priority_insights(llm_insights)

        if not all_insights:
            return self._generate_basic_priority_actions(data)

        return sorted(all_insights, key=lambda x: (x.get('impact', 0) * x.get('confidence', 0)), reverse=True)[:5]

    def _get_priority_insights(self, insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract priority insights from a set of insights."""
        priority_insights = []

        for category in ['technical_insights', 'content_insights', 'backlink_insights']:
            for insight in insights.get(category, []):
                if insight.get('impact', 0) > 0.7:
                    priority_insights.append(insight)

        return priority_insights

    def _generate_basic_insights(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback basic insights when AI fails."""
        return {
            'technical_insights': self._basic_technical_insights(data),
            'content_insights': self._basic_content_insights(data),
            'backlink_insights': self._basic_backlink_insights(data),
            'priority_actions': self._generate_priority_actions(data, {}, {})
        }

    def _basic_technical_insights(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fallback technical SEO insights."""
        return [{'type': 'technical', 'metric': 'meta_description', 'recommendation': 'Add a relevant meta description for better SEO.', 'priority': 'high', 'impact': 0.8}]

    def _basic_content_insights(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fallback content SEO insights."""
        return [{'type': 'content', 'metric': 'word_count', 'recommendation': 'Increase content length to at least 300 words.', 'priority': 'high', 'impact': 0.7}]

    def _basic_backlink_insights(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fallback backlink insights."""
        return [{'type': 'backlinks', 'metric': 'total_links', 'recommendation': 'Increase backlinks to improve authority.', 'priority': 'high', 'impact': 0.9}]
