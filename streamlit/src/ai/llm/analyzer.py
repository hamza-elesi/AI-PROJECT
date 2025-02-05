# src/ai/llm/analyzer.py

from typing import Dict, Any, List
import openai
from utils.token_counter import TokenCounter
from utils.cost_optimizer import CostOptimizer

class LLMAnalyzer:
    """Handles selective LLM analysis of SEO data"""
    
    def __init__(self):
        self.token_counter = TokenCounter()
        self.cost_optimizer = CostOptimizer()
        self.model = "gpt-3.5-turbo"  # Default model for cost efficiency

    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Selectively analyze SEO data using LLM
        Only processes complex patterns that need advanced analysis
        """
        analysis_needed = self.cost_optimizer.should_analyze(data)
        if not analysis_needed:
            return {'type': 'basic', 'insights': []}

        try:
            technical_insights = await self._analyze_technical_seo(data.get('technical_seo', {}))
            content_insights = await self._analyze_content(data.get('scraped_data', {}))
            strategy_insights = await self._generate_strategy(data)

            return {
                'type': 'enhanced',
                'technical_insights': technical_insights,
                'content_insights': content_insights,
                'strategy_recommendations': strategy_insights
            }
        except Exception as e:
            return {'error': str(e), 'type': 'basic', 'insights': []}

    async def _analyze_technical_seo(self, technical_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze complex technical SEO patterns"""
        prompt = self._create_technical_prompt(technical_data)
        if not self.token_counter.within_limits(prompt):
            return []

        response = await self._get_llm_response(prompt)
        return self._parse_technical_response(response)

    async def _analyze_content(self, content_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze content quality and structure"""
        prompt = self._create_content_prompt(content_data)
        if not self.token_counter.within_limits(prompt):
            return []

        response = await self._get_llm_response(prompt)
        return self._parse_content_response(response)

    async def _generate_strategy(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate strategic recommendations"""
        prompt = self._create_strategy_prompt(data)
        if not self.token_counter.within_limits(prompt):
            return []

        response = await self._get_llm_response(prompt)
        return self._parse_strategy_response(response)

    def _create_technical_prompt(self, data: Dict[str, Any]) -> str:
        return f"""
        Analyze the following technical SEO data and provide specific improvements:
        {data}
        Focus on critical issues and prioritize recommendations.
        """

    def _create_content_prompt(self, data: Dict[str, Any]) -> str:
        return f"""
        Analyze the following content data and provide optimization suggestions:
        {data}
        Focus on readability, structure, and SEO optimization.
        """

    def _create_strategy_prompt(self, data: Dict[str, Any]) -> str:
        return f"""
        Based on the following SEO data:
        {data}
        Provide strategic recommendations for improvement.
        Focus on actionable steps and prioritize by impact.
        """

    async def _get_llm_response(self, prompt: str) -> str:
        """Get response from OpenAI API"""
        try:
            response = await openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert SEO analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"LLM API error: {str(e)}")

    def _parse_technical_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse technical analysis response"""
        # Implement parsing logic
        pass

    def _parse_content_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse content analysis response"""
        # Implement parsing logic
        pass

    def _parse_strategy_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse strategy recommendations response"""
        # Implement parsing logic
        pass