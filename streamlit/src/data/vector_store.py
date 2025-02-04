from chromadb import Client
from chromadb.config import Settings
from langchain.embeddings.openai import OpenAIEmbeddings
import os

class VectorStore:
    def __init__(self):
        self.client = Client(
            Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory="vector_store"
            )
        )
        self.collection_name = "seo_knowledge"
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embeddings.embed_query
        )

    def add_documents(self, documents):
        """Add documents to the vector store."""
        for doc in documents:
            self.collection.add(
                documents=[doc["content"]],
                metadatas=[doc["metadata"]],
                ids=[doc["id"]]
            )

    def query(self, query: str, top_k: int = 5):
        """Query the vector store."""
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        return results

    def persist(self):
        """Persist the vector store."""
        self.client.persist()
