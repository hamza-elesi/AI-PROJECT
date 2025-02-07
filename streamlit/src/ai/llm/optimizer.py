from typing import Dict, Any
import json
from datetime import datetime, timedelta


class CostOptimizer:
    """Optimizes LLM usage and controls costs."""

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = {}  # Ensure config is not None

        self.max_daily_requests = config.get("max_requests_per_day", 100)
        self.token_buffer = config.get("token_buffer", 0.9)  # 90% of max tokens
        self.complexity_threshold = config.get("complexity_threshold", 0.6)
        self.usage_history = {}
        self.last_reset = datetime.now().date()

        print("✅ CostOptimizer Initialized Successfully")

    def should_use_llm(self, data: Dict[str, Any]) -> bool:
        """Determine if LLM analysis is needed based on complexity and quotas."""
        # ✅ Check daily quota
        if not self._check_daily_quota():
            print("⚠️ LLM request skipped due to quota limits.")
            return False

        # ✅ Check data complexity
        complexity_score = self._calculate_complexity(data)
        print(f"🔹 Complexity Score: {complexity_score:.2f} (Threshold: {self.complexity_threshold})")
        
        return complexity_score > self.complexity_threshold

    def track_usage(self, tokens_used: int, cost: float):
        """Track API usage and costs."""
        today = datetime.now().date()

        # ✅ Reset daily tracking if needed
        if today > self.last_reset:
            self.usage_history = {}
            self.last_reset = today

        # ✅ Update usage stats
        if today not in self.usage_history:
            self.usage_history[today] = {"requests": 0, "tokens": 0, "cost": 0.0}

        self.usage_history[today]["requests"] += 1
        self.usage_history[today]["tokens"] += tokens_used
        self.usage_history[today]["cost"] += cost

        print(f"🟢 LLM Usage Updated: {self.usage_history[today]}")

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics."""
        today = datetime.now().date()
        return self.usage_history.get(today, {"requests": 0, "tokens": 0, "cost": 0.0})

    def _check_daily_quota(self) -> bool:
        """Check if within daily request quota."""
        today = datetime.now().date()
        current_requests = self.usage_history.get(today, {}).get("requests", 0)
        return current_requests < self.max_daily_requests

    def _calculate_complexity(self, data: Dict[str, Any]) -> float:
        """Calculate complexity score of the data."""
        complexity_scores = []

        # ✅ Technical SEO complexity
        if "technical_seo" in data:
            tech_score = self._calculate_technical_complexity(data["technical_seo"])
            complexity_scores.append(tech_score)

        # ✅ Content complexity
        if "scraped_data" in data:
            content_score = self._calculate_content_complexity(data["scraped_data"])
            complexity_scores.append(content_score)

        # ✅ Avoid division by zero
        if complexity_scores:
            avg_complexity = sum(complexity_scores) / len(complexity_scores)
        else:
            avg_complexity = 0.0

        return avg_complexity

    def _calculate_technical_complexity(self, tech_data: Dict[str, Any]) -> float:
        """Calculate technical SEO complexity."""
        score = 0.0
        factors = 0

        # ✅ Meta tags complexity
        if "meta_tags" in tech_data:
            meta_tags = tech_data["meta_tags"]
            if not meta_tags.get("meta_description"):
                score += 0.8  # Missing meta description increases complexity
            if len(meta_tags.get("title", "")) > 60:
                score += 0.6  # Long title needs analysis
            factors += 2

        # ✅ Heading structure complexity
        if "headings" in tech_data:
            headings = tech_data["headings"]
            if headings.get("h1", 0) != 1:
                score += 0.7  # Incorrect H1 usage
            if sum(headings.values()) > 15:
                score += 0.5  # Complex heading structure
            factors += 2

        return score / factors if factors > 0 else 0.0

    def _calculate_content_complexity(self, content_data: Dict[str, Any]) -> float:
        """Calculate content complexity."""
        score = 0.0
        factors = 0

        # ✅ Content length complexity
        if "content" in content_data:
            content = content_data["content"]
            word_count = content.get("word_count", 0)
            if word_count > 1000:
                score += 0.8  # Long content needs more analysis
            elif word_count < 300:
                score += 0.6  # Too short content needs recommendations
            factors += 1

        # ✅ Structure complexity
        if "paragraphs" in content_data.get("content", {}):
            if content_data["content"]["paragraphs"] > 10:
                score += 0.7  # Complex structure
            factors += 1

        return score / factors if factors > 0 else 0.0

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text."""
        # ✅ Rough estimation: ~4 characters per token
        return len(text) // 4

    def optimize_prompt(self, prompt: str, max_tokens: int) -> str:
        """Optimize prompt to fit within token limits."""
        estimated_tokens = self.estimate_tokens(prompt)

        if estimated_tokens <= max_tokens:
            return prompt

        # ✅ Truncate while maintaining crucial information
        ratio = max_tokens / estimated_tokens
        truncate_length = int(len(prompt) * ratio * self.token_buffer)
        optimized_prompt = prompt[:truncate_length]

        print(f"🔹 Optimized Prompt (Tokens: {estimated_tokens} → {max_tokens}):\n{optimized_prompt[:500]}...")

        return optimized_prompt
