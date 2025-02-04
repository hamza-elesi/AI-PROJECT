from typing import Dict, Any
from rag.rag_pipeline import RAGPipeline

class InsightGenerator:
    def __init__(self, rag_pipeline: RAGPipeline):
        self.rag_pipeline = rag_pipeline

    def generate_insights(self, query: str, data: Dict[str, Any]) -> str:
        """
        Generate actionable insights using the RAG pipeline.
        :param query: The user query for insight generation.
        :param data: The SEO analysis data.
        :return: Generated insights.
        """
        # Format data and store it in the knowledge base
        seo_knowledge = self.rag_pipeline.add_to_knowledge_base(data)
        response = self.rag_pipeline.query_knowledge_base(query)
        return response
