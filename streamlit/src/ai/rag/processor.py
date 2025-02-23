from typing import Dict, Any, List
from .knowledge_base import SEOKnowledgeBase
from .vector_store import VectorStore


class RAGProcessor:
    """Processes SEO data using RAG system."""
    
    def __init__(self):
        self.knowledge_base = SEOKnowledgeBase()
        self.vector_store = VectorStore()

    # async def process(self, seo_data: Dict[str, Any]) -> Dict[str, Any]:
    #     """Process SEO data and generate enhanced insights."""
    #     print("🟢 Starting RAG Processing...")
    #     print("\n=== Starting RAG Processing Debug ===")
        
    #     technical_data = seo_data.get('technical_seo', {}).get('metrics', {})
    #     content_data = seo_data.get('content_data', {}).get('metrics', {})
    #     backlink_data = seo_data.get('backlink_data', {}).get('metrics', {}) 


    #     # Get relevant insights with structured data
    #     technical_insights = await self._analyze_technical(technical_data)
    #     content_insights = await self._analyze_content(content_data)
    #     backlink_insights = await self._analyze_backlinks(backlink_data)


    #     # Debugging: Check if insights are being generated
    #     print(f"🔹 Technical Insights: {technical_insights}")
    #     print(f"🔹 Content Insights: {content_insights}")
    #     print(f"🔹 Backlink Insights: {backlink_insights}")
        
    #     # Find similar cases
    #     similar_cases = self.vector_store.find_similar(seo_data)

    #     # Debugging: Check if similar cases are found
    #     print(f"🔹 Similar Cases: {similar_cases}")

    #     # Store new case in vector store
    #     self._store_embeddings(seo_data)

    #     # Ensure no empty insights
    #     if not technical_insights:
    #         print("⚠️ No technical insights found. Using fallback recommendations.")
    #         technical_insights = self._generate_fallback_technical_insights(seo_data)

    #     if not content_insights:
    #         print("⚠️ No content insights found. Using fallback recommendations.")
    #         content_insights = self._generate_fallback_content_insights(seo_data)

    #     if not backlink_insights:
    #         print("⚠️ No backlink insights found. Using fallback recommendations.")
    #         backlink_insights = self._generate_fallback_backlink_insights(seo_data)

    #     return {
    #         'technical_insights': technical_insights,
    #         'content_insights': content_insights,
    #         'backlink_insights': backlink_insights,
    #         'similar_cases': similar_cases
    #     }


    # Modify the process method in RAGProcessor class
    async def process(self, seo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process SEO data and generate enhanced insights."""
        print("🟢 Starting RAG Processing...")
        print("\n=== Starting RAG Processing Debug ===")
        
        technical_data = seo_data.get('technical_seo', {}).get('metrics', {})
        content_data = seo_data.get('content_data', {}).get('metrics', {})
        backlink_data = seo_data.get('backlink_data', {}).get('metrics', {}) 

        # Get relevant insights with structured data
        technical_insights = await self._analyze_technical(technical_data)
        content_insights = await self._analyze_content(content_data)
        backlink_insights = await self._analyze_backlinks(backlink_data)

        # Debugging: Check if insights are being generated
        print(f"🔹 Technical Insights: {technical_insights}")
        print(f"🔹 Content Insights: {content_insights}")
        print(f"🔹 Backlink Insights: {backlink_insights}")
        
        # Find similar cases
        similar_cases = self.vector_store.find_similar(seo_data)

        # Debugging: Check if similar cases are found
        print(f"🔹 Similar Cases: {similar_cases}")

        # Store new case in vector store
        self._store_embeddings(seo_data)

        # Ensure no empty insights
        if not technical_insights:
            print("⚠️ No technical insights found. Using fallback recommendations.")
            technical_insights = self._generate_fallback_technical_insights(seo_data)

        if not content_insights:
            print("⚠️ No content insights found. Using fallback recommendations.")
            content_insights = self._generate_fallback_content_insights(seo_data)

        if not backlink_insights:
            print("⚠️ No backlink insights found. Using fallback recommendations.")
            backlink_insights = self._generate_fallback_backlink_insights(seo_data)

        # Create response dict
        response_dict = {
            'technical_insights': technical_insights,
            'content_insights': content_insights,
            'backlink_insights': backlink_insights,
            'similar_cases': similar_cases
        }
        
        # Validate with Pydantic
        try:
            from src.models.seo_models import RAGResponse
            validated_response = RAGResponse(**response_dict)
            return validated_response.dict()
        except Exception as e:
            print(f"⚠️ RAG Response validation error: {e}, returning unvalidated data")
            return response_dict

    async def _analyze_technical(self, technical_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze technical SEO aspects."""
        insights = self.knowledge_base.get_recommendations('technical', technical_data)
        return insights if insights else []

    async def _analyze_content(self, content_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze content aspects."""
        insights = self.knowledge_base.get_recommendations('content', content_data)
        return insights if insights else []

    async def _analyze_backlinks(self, backlink_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze backlink profile."""
        insights = self.knowledge_base.get_recommendations('backlinks', backlink_data)
        return insights if insights else []

    def _store_embeddings(self, seo_data: Dict[str, Any]):
        """Store new SEO data embeddings in vector store."""
        try:
            self.vector_store.add_embeddings(seo_data, 'analysis')
            print("✅ Successfully stored SEO data in vector store.")
        except Exception as e:
            print(f"❌ Error storing embeddings: {e}")

    def _generate_fallback_technical_insights(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate basic fallback technical insights."""
        fallback_insights = []

        meta_tags = data.get('scraped_data', {}).get('meta_tags', {})
        if not meta_tags.get('meta_description'):
            fallback_insights.append({
                'type': 'technical',
                'metric': 'meta_description',
                'recommendation': 'Add a relevant meta description for better SEO.',
                'priority': 'high',
                'impact': 0.8
            })

        return fallback_insights

    def _generate_fallback_content_insights(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate basic fallback content insights."""
        fallback_insights = []

        content_data = data.get('scraped_data', {}).get('content', {})
        word_count = content_data.get('word_count', 0)
        if word_count < 300:
            fallback_insights.append({
                'type': 'content',
                'metric': 'word_count',
                'recommendation': 'Increase content length to at least 300 words.',
                'priority': 'high',
                'impact': 0.7
            })

        return fallback_insights

    def _generate_fallback_backlink_insights(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate basic fallback backlink insights."""
        fallback_insights = []

        moz_metrics = data.get('moz_data', {}).get('metrics', {})
        if moz_metrics.get('total_links', 0) < 5:
            fallback_insights.append({
                'type': 'backlinks',
                'metric': 'total_links',
                'recommendation': 'Increase the number of quality backlinks to improve authority.',
                'priority': 'high',
                'impact': 0.9
            })

        return fallback_insights
