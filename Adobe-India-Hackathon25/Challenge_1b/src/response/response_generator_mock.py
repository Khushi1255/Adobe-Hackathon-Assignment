"""
Mock Response Generator for Challenge 1b - No LLM dependencies
"""

from langchain.schema import Document
from typing import List, Dict, Optional
import logging

class MockResponseGenerator:
    """
    Mock response generator that doesn't require LLM server
    """
    
    def __init__(self, config: Dict):
        """
        Initialize the mock response generator.
        
        Args:
            config (Dict): Configuration dictionary (not used in mock)
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def generate_answer(self, 
                       query: str,
                       relevant_chunks: List[Document],
                       metadata: Optional[Dict] = None) -> Dict:
        """
        Generate a mock answer based on retrieved document chunks.
        """
        try:
            context = self._prepare_context(relevant_chunks)
            response = self._generate_response(query, context)
            
            return {
                'response': response,
                'source_documents': [doc.metadata for doc in relevant_chunks],
                'metadata': metadata or {}
            }
            
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            return {
                'response': "I apologize, but I encountered an error generating a response. Please try again.",
                'error': str(e),
                'metadata': metadata or {}
            }

    def _prepare_context(self, chunks: List[Document]) -> str:
        """
        Prepare structured context from retrieved document chunks.
        """
        context_parts = []
        
        for i, chunk in enumerate(chunks, 1):
            source_info = f"Source: {chunk.metadata.get('source', 'Unknown')}"
            context_parts.append(f"[{i}] {source_info}\n{chunk.page_content}")
        
        return "\n\n".join(context_parts)

    def _generate_response(self, query: str, context: str) -> str:
        """
        Generate mock response based on query and context.
        """
        return f"Based on the provided information, here are the key points related to '{query}':\n\n{context[:500]}..."

    def generate_refined_text(self, content: str, title: str) -> str:
        """
        Generate mock refined text analysis for a section.
        """
        return f"Refined analysis of '{title}': {content[:200]}..."
    
    def expand_query(self, query: str) -> str:
        """
        Return original query (no expansion in mock).
        """
        return query 