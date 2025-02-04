from data.vector_store import VectorStore

class SEOKnowledgeBase:
    def __init__(self):
        self.vector_store = VectorStore()

    def add_data(self, seo_data: dict):
        """Add SEO data to the knowledge base."""
        documents = [
            {
                "content": seo_data.get("scraped_data", {}).get("meta_tags", {}).get("title", ""),
                "metadata": {"type": "Meta Tags", "url": seo_data["url"]},
                "id": f"meta_tags_{seo_data['url']}"
            },
            {
                "content": seo_data.get("scraped_data", {}).get("content", {}).get("text", ""),
                "metadata": {"type": "Content", "url": seo_data["url"]},
                "id": f"content_{seo_data['url']}"
            }
        ]
        self.vector_store.add_documents(documents)
        self.vector_store.persist()

    def query_data(self, query: str):
        """Query the knowledge base."""
        return self.vector_store.query(query)
