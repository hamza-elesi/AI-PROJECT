from typing import Dict, Any, List
from .knowledge_base import SEOKnowledgeBase
from .vector_store import VectorStore

class RAGProcessor:
    """Processes SEO data using RAG system."""
    
    def __init__(self):
        self.knowledge_base = SEOKnowledgeBase()
        self.vector_store = VectorStore()

    async def process(self, seo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process SEO data and generate enhanced insights."""
        # Get relevant guidelines
        technical_insights = await self._analyze_technical(seo_data.get('technical_seo', {}))
        content_insights = await self._analyze_content(seo_data.get('scraped_data', {}))
        backlink_insights = await self._analyze_backlinks(seo_data.get('moz_data', {}))

        # Debugging: Check if insights are being generated
        print("🟢 Technical Insights:", technical_insights)
        print("🟢 Content Insights:", content_insights)
        print("🟢 Backlink Insights:", backlink_insights)
        
        # Find similar cases
        similar_cases = self.vector_store.find_similar(seo_data)

        # Debugging: Check if similar cases are found
        print("🟢 Similar Cases:", similar_cases)

        # Store new case
        self.vector_store.add_embeddings(seo_data, 'analysis')

        return {
            'technical_insights': technical_insights,
            'content_insights': content_insights,
            'backlink_insights': backlink_insights,
            'similar_cases': similar_cases
        }

    async def _analyze_technical(self, technical_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze technical SEO aspects."""
        guidelines = self.knowledge_base.get_guidelines('technical', 'best_practices')
        return self.knowledge_base.get_recommendations('technical', technical_data)

    async def _analyze_content(self, content_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze content aspects."""
        guidelines = self.knowledge_base.get_guidelines('content', 'best_practices')
        return self.knowledge_base.get_recommendations('content', content_data)

    async def _analyze_backlinks(self, backlink_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze backlink profile."""
        guidelines = self.knowledge_base.get_guidelines('backlinks', 'quality_metrics')
        return self.knowledge_base.get_recommendations('backlinks', backlink_data)
