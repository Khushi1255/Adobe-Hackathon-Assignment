"""
Configuration class for Challenge 1b - CPU-only version
"""

import os
from typing import Dict, Any

class Config:
    """
    Configuration class for Challenge 1b with CPU-only settings
    """
    
    def __init__(self):
        # Default CPU-only configuration
        self.config = {
            'paths': {
                'cache_dir': './cache',
                'log_dir': './logs',
                'data_dir': './data'
            },
            'model': {
                'embedding_model_hf': 'sentence-transformers/all-MiniLM-L6-v2',
                'rerank_model': 'cross-encoder/ms-marco-MiniLM-L-6-v2',
                'device_rerank': 'cpu',  # CPU-only
                'device_embedding': 'cpu'  # CPU-only
            },
            'processing': {
                'batch_size_embeddings': 32,
                'batch_size_reranking': 16,
                'use_parent_document_retriever': False,
                'parent_chunk_size': 2000,
                'child_chunk_size': 400,
                'OMP_NUM_THREADS': 4
            },
            'retrieval': {
                'bm25_weight': 0.3,
                'vector_weight': 0.7,
                'top_k': 10,
                'llamafile_server_base_url': 'http://localhost:8080'
            },
            'logging': {
                'level': 'INFO',
                'show_progress': True
            }
        }
        
        # Create necessary directories
        for path_key in ['cache_dir', 'log_dir', 'data_dir']:
            path = self.config['paths'][path_key]
            os.makedirs(path, exist_ok=True)
    
    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-style access to config"""
        return self.config[key]
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value with default"""
        return self.config.get(key, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """Return config as dictionary"""
        return self.config.copy() 