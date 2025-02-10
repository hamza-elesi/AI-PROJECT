from typing import Dict, Any

class CostOptimizer:
    """Optimizes LLM usage based on data complexity"""

    def __init__(self):
        self.complexity_thresholds = {
            'technical': 0.2,
            'content': 0.2,
            'backlinks': 0.2
        }

    def should_use_llm(self, data: Dict[str, Any]) -> bool:
        """Determine if LLM analysis is needed based on data complexity"""
        complexity_score = self._calculate_complexity(data)

        print(f"🔹 Complexity Score Calculated: {complexity_score} (Threshold: 0.5)")

        if complexity_score > 0.2:
            print("🟢 LLM analysis is REQUIRED for this data.")
            return True
        else:
            print("⚠️ LLM analysis is NOT required (complexity too low).")
            return False

    def _calculate_complexity(self, data: Dict[str, Any]) -> float:
        """Calculate overall data complexity score"""
        scores = []

        if 'technical_seo' in data:
            tech_complexity = self._technical_complexity(data['technical_seo'])
            print(f"🔸 Technical Complexity: {tech_complexity}")
            scores.append(tech_complexity)

        if 'scraped_data' in data:
            content_complexity = self._content_complexity(data['scraped_data'])
            print(f"🔸 Content Complexity: {content_complexity}")
            scores.append(content_complexity)

        if 'moz_data' in data:
            backlink_complexity = self._backlink_complexity(data['moz_data'])
            print(f"🔸 Backlink Complexity: {backlink_complexity}")
            scores.append(backlink_complexity)

        return sum(scores) / len(scores) if scores else 0.0

    def _technical_complexity(self, data: Dict[str, Any]) -> float:
        """Determine technical SEO complexity based on missing elements"""
        score = 0.0
        factors = 0

        if not data.get("meta_description"):
            score += 0.8  # High complexity if missing meta description
        if not data.get("canonical"):
            score += 0.6  # Medium complexity if missing canonical tag
        if data.get("errors", 0) > 5:
            score += 0.9  # High complexity if many SEO errors

        factors += 3  # We checked 3 factors
        return score / factors if factors else 0.0

    def _content_complexity(self, data: Dict[str, Any]) -> float:
        """Determine content SEO complexity"""
        score = 0.0
        factors = 0

        if data.get("word_count", 0) < 300:
            score += 0.7  # Penalize if content is too short
        if len(data.get("headings", {}).keys()) < 2:
            score += 0.5  # Penalize if not enough headings
        if not data.get("alt_texts"):
            score += 0.6  # Penalize if images have no alt texts

        factors += 3  # We checked 3 factors
        return score / factors if factors else 0.0

    def _backlink_complexity(self, data: Dict[str, Any]) -> float:
        """Determine backlink profile complexity"""
        score = 0.0
        factors = 0

        if data.get("total_links", 0) < 10:
            score += 0.8  # High complexity if very few backlinks
        if data.get("spam_score", 0) > 30:
            score += 0.7  # Penalize if spam score is high
        if data.get("linking_domains", 0) < 5:
            score += 0.6  # Penalize if very few linking domains

        factors += 3  # We checked 3 factors
        return score / factors if factors else 0.0
