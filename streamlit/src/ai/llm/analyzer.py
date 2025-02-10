from typing import Dict, Any, List
import openai
import json
import asyncio
from src.utils.token_counter import TokenCounter  # ✅ Token limiter

class LLMAnalyzer:
    """Handles selective LLM analysis of SEO data."""

    def __init__(self):
        self.token_counter = TokenCounter()
        self.model = "gpt-3.5-turbo"  # ✅ Default to cost-efficient model
        print("✅ LLMAnalyzer Initialized Successfully")

    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run LLM analysis with JSON-formatted output.
        """
        try:
            print("🟢 Starting LLM Analysis (FORCED)...")  # ✅ LLM will always run

            technical_insights = await self._analyze_technical_seo(data.get('technical_seo', {}))
            content_insights = await self._analyze_content(data.get('scraped_data', {}))
            strategy_insights = await self._generate_strategy(data)

            print(f"✅ LLM Analysis Completed! Technical: {len(technical_insights)}, Content: {len(content_insights)}, Strategy: {len(strategy_insights)}")

            return {
                'type': 'enhanced',
                'technical_insights': technical_insights,
                'content_insights': content_insights,
                'strategy_recommendations': strategy_insights
            }
        except Exception as e:
            print(f"❌ LLM Analysis Error: {e}")
            return {'error': str(e), 'type': 'basic', 'insights': []}

    async def _analyze_technical_seo(self, technical_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze complex technical SEO patterns"""
        prompt = self._create_technical_prompt(technical_data)
        if not self.token_counter.within_limits(prompt):
            print("⚠️ LLM request skipped: Token limit exceeded.")
            return []

        response = await self._get_llm_response(prompt)
        return self._parse_llm_response(response)

    async def _analyze_content(self, content_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze content quality and structure"""
        prompt = self._create_content_prompt(content_data)
        if not self.token_counter.within_limits(prompt):
            print("⚠️ LLM request skipped: Token limit exceeded.")
            return []

        response = await self._get_llm_response(prompt)
        return self._parse_llm_response(response)

    async def _generate_strategy(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate strategic recommendations"""
        prompt = self._create_strategy_prompt(data)
        if not self.token_counter.within_limits(prompt):
            print("⚠️ LLM request skipped: Token limit exceeded.")
            return []

        response = await self._get_llm_response(prompt)
        return self._parse_llm_response(response)

    async def _get_llm_response(self, prompt: str) -> str:
        """Get response from OpenAI API"""
        try:
            print("🔄 Sending request to OpenAI API (Forced Run)...")
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert SEO analyst. Provide insights in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},  # ✅ Enforce JSON response format
                temperature=0.7,
                max_tokens=800  # ✅ Increased token count for more detailed responses
            )

            content = response.choices[0].message.content.strip()
            print(f"✅ OpenAI JSON Response:\n{content}\n")
            return content  # ✅ Ensure response is returned correctly

        except Exception as e:
            print(f"❌ OpenAI API Error: {e}")
            return ""

    def _parse_llm_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse response from OpenAI API"""
        try:
            if not response.strip():
                print("⚠️ Empty response from LLM. Returning empty insights.")
                return []

            # ✅ Convert JSON string to Python object
            parsed_data = json.loads(response)

            # ✅ Ensure output is a list
            if isinstance(parsed_data, dict) and "recommendations" in parsed_data:
                return parsed_data["recommendations"]

            if isinstance(parsed_data, dict) and "improvements" in parsed_data:
                return parsed_data["improvements"]

            if isinstance(parsed_data, dict) and "actionable_steps" in parsed_data:
                return parsed_data["actionable_steps"]

            print("⚠️ LLM response format is incorrect. Returning empty insights.")
        except json.JSONDecodeError as e:
            print(f"❌ JSON Parsing Error: {e}")
        return []

    def _create_technical_prompt(self, data: Dict[str, Any]) -> str:
        """Generate LLM prompt for technical SEO analysis"""
        return json.dumps({
            "task": "Analyze technical SEO",
            "data": data,
            "instructions": "Provide a list of specific recommendations to improve technical SEO. Format the response as a JSON object with a 'recommendations' key."
        }, indent=2)

    def _create_content_prompt(self, data: Dict[str, Any]) -> str:
        """Generate LLM prompt for content SEO analysis"""
        return json.dumps({
            "task": "Analyze content SEO",
            "data": data,
            "instructions": "Provide a list of improvements focusing on keyword optimization, readability, and structure. Format the response as a JSON object with an 'improvements' key."
        }, indent=2)

    def _create_strategy_prompt(self, data: Dict[str, Any]) -> str:
        """Generate LLM prompt for strategic SEO recommendations"""
        return json.dumps({
            "task": "Generate strategic SEO recommendations",
            "data": data,
            "instructions": "Provide a list of actionable steps for improving ranking and visibility. Format the response as a JSON object with an 'actionable_steps' key."
        }, indent=2)
