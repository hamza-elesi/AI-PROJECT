# src/config/ai_config.py

from typing import Dict, Any
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

class AIConfig:
    """Configuration settings for AI components"""
    
    def __init__(self):
        # Base paths
        self.knowledge_base_path = Path(__file__).parent.parent / 'knowledge'
        
        # ChromaDB settings
        self.chromadb_settings = {
            'collection_name': 'seo_guidelines',
            'persist_directory': str(self.knowledge_base_path / 'embeddings'),
            'metadata': {'description': 'SEO best practices and recommendations'}
        }
        
        # RAG settings
        self.rag_settings = {
            'similarity_threshold': 0.75,
            'max_results': 5,
            'guidelines_paths': {
                'technical': str(self.knowledge_base_path / 'seo_guidelines' / 'technical_seo.json'),
                'content': str(self.knowledge_base_path / 'seo_guidelines' / 'content_seo.json')
            }
        }
        
        # LLM settings
        self.llm_settings = {
            'model': 'gpt-3.5-turbo',
            'max_tokens': 500,
            'temperature': 0.7,
            'token_limit': 4000,
            'api_key': os.getenv('OPENAI_API_KEY')
        }
        
        # Cost optimization settings
        self.cost_settings = {
            'max_requests_per_day': 100,
            'token_buffer': 0.9,  # 90% of max tokens
            'complexity_threshold': 0.6
        }

    def get_chromadb_config(self) -> Dict[str, Any]:
        """Get ChromaDB configuration"""
        return self.chromadb_settings

    def get_rag_config(self) -> Dict[str, Any]:
        """Get RAG system configuration"""
        return self.rag_settings

    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration"""
        return self.llm_settings

    def get_cost_config(self) -> Dict[str, Any]:
        """Get cost optimization configuration"""
        return self.cost_settings

    def validate_config(self) -> bool:
        """Validate configuration settings"""
        try:
            # Check paths exist
            for path in self.rag_settings['guidelines_paths'].values():
                if not Path(path).exists():
                    raise FileNotFoundError(f"Guidelines file not found: {path}")

            # Check API key
            if not self.llm_settings['api_key']:
                raise ValueError("OpenAI API key not found in environment")

            # Validate thresholds
            if not 0 <= self.rag_settings['similarity_threshold'] <= 1:
                raise ValueError("Similarity threshold must be between 0 and 1")

            if not 0 <= self.cost_settings['complexity_threshold'] <= 1:
                raise ValueError("Complexity threshold must be between 0 and 1")

            return True

        except Exception as e:
            print(f"Configuration validation failed: {str(e)}")
            return False

    def update_settings(self, category: str, updates: Dict[str, Any]) -> bool:
        """Update configuration settings"""
        try:
            if category == 'rag':
                self.rag_settings.update(updates)
            elif category == 'llm':
                self.llm_settings.update(updates)
            elif category == 'cost':
                self.cost_settings.update(updates)
            elif category == 'chromadb':
                self.chromadb_settings.update(updates)
            else:
                raise ValueError(f"Unknown category: {category}")

            return True

        except Exception as e:
            print(f"Failed to update settings: {str(e)}")
            return False

    def get_guideline_path(self, category: str) -> str:
        """Get path for specific guideline category"""
        return self.rag_settings['guidelines_paths'].get(category, '')