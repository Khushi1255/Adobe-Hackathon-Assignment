"""
Response Generator for Challenge 1b
Wrapper around ResponseGenerator for compatibility
"""

from .response_generator import ResponseGenerator
from typing import List, Dict, Any

class Generator:
    """
    Generator for Challenge 1b
    Wraps ResponseGenerator functionality
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = {
                'retrieval': {
                    'llamafile_server_base_url': 'http://localhost:8080'
                }
            }
        self.response_generator = ResponseGenerator(config)
    
    def generate_response(self, query: str, documents: List[Any]) -> str:
        """
        Generate response based on query and documents
        
        Args:
            query: Search query
            documents: List of relevant documents
            
        Returns:
            Generated response text
        """
        try:
            return self.response_generator.generate_response(query, documents)
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Unable to generate response at this time."
    
    def generate_summary(self, documents: List[Any]) -> str:
        """
        Generate summary of documents
        
        Args:
            documents: List of documents to summarize
            
        Returns:
            Generated summary text
        """
        try:
            return self.response_generator.generate_summary(documents)
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Unable to generate summary at this time." 