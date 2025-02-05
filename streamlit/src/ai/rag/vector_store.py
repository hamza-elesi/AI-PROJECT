# src/ai/rag/vector_store.py

from typing import Dict, Any, List, Optional
import numpy as np
from pathlib import Path
import json
import chromadb
from chromadb.config import Settings

class VectorStore:
    """Manages embeddings and similarity search for SEO data"""
    
    def __init__(self):
        self.client = chromadb.Client(Settings(
            persist_directory=str(Path(__file__).parent.parent.parent / 'knowledge' / 'embeddings')
        ))
        self.collection = self.client.get_or_create_collection("seo_embeddings")

    async def add_embeddings(self, data: Dict[str, Any], category: str):
        """Add new embeddings to the store"""
        # Convert data to format suitable for embeddings
        documents = self._prepare_documents(data)
        metadatas = [{"category": category} for _ in documents]
        ids = [f"{category}_{i}" for i in range(len(documents))]
        
        # Add to collection
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    async def find_similar(self, query_data: Dict[str, Any], n_results: int = 5) -> List[Dict[str, Any]]:
        """Find similar cases based on query data"""
        query = self._prepare_query(query_data)
        
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return self._process_results(results)

    def _prepare_documents(self, data: Dict[str, Any]) -> List[str]:
        """Prepare data for embedding"""
        documents = []
        
        for key, value in data.items():
            if isinstance(value, dict):
                documents.extend(self._prepare_documents(value))
            else:
                documents.append(f"{key}: {value}")
                
        return documents

    def _prepare_query(self, data: Dict[str, Any]) -> str:
        """Convert query data to string format"""
        query_parts = []
        
        for key, value in data.items():
            if isinstance(value, dict):
                query_parts.extend(self._prepare_query(value).split('\n'))
            else:
                query_parts.append(f"{key}: {value}")
                
        return '\n'.join(query_parts)

    def _process_results(self, results: Dict) -> List[Dict[str, Any]]:
        """Process and structure similarity search results"""
        processed_results = []
        
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            processed_results.append({
                'content': doc,
                'category': metadata['category'],
                'similarity_score': 1 - distance,  # Convert distance to similarity
                'rank': i + 1
            })
            
        return processed_results