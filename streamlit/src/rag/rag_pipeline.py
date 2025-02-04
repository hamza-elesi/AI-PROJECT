from rag.openai_client import OpenAIClient
from rag.seo_knowledge_base import SEOKnowledgeBase

class RAGPipeline:
    def __init__(self):
        self.knowledge_base = SEOKnowledgeBase()
        self.openai_client = OpenAIClient()

    def add_to_knowledge_base(self, seo_data: dict):
        """Add SEO data to the knowledge base."""
        self.knowledge_base.add_data(seo_data)

    def query_knowledge_base(self, query: str) -> str:
        """Query the knowledge base and generate a response."""
        # Retrieve relevant data from the knowledge base
        retrieved_docs = self.knowledge_base.query_data(query)
        prompt = f"The following SEO data has been retrieved:\n\n{retrieved_docs}\n\nAnswer the following query: {query}"
        response = self.openai_client.generate_response(prompt)
        return response
