"""
Lightweight vector search service using scikit-learn instead of FAISS
For deployment environments where FAISS compilation fails
"""
import logging
import numpy as np
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class LightweightVectorSearch:
    """
    Lightweight vector search using TF-IDF and cosine similarity
    Alternative to FAISS for deployment environments
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            max_df=0.8,
            min_df=2
        )
        self.chunk_vectors = None
        self.chunks = []
        self.is_fitted = False
        
        logger.info("Initialized lightweight vector search with TF-IDF")
    
    def create_index(self, chunks: List[str]) -> bool:
        """
        Create TF-IDF index from text chunks
        
        Args:
            chunks: List of text chunks
            
        Returns:
            bool: True if successful
        """
        try:
            logger.info(f"Creating TF-IDF index for {len(chunks)} chunks")
            
            self.chunks = chunks
            
            # Create TF-IDF vectors
            self.chunk_vectors = self.vectorizer.fit_transform(chunks)
            self.is_fitted = True
            
            logger.info(f"TF-IDF index created successfully with {self.chunk_vectors.shape[1]} features")
            return True
            
        except Exception as e:
            logger.error(f"Error creating TF-IDF index: {str(e)}")
            return False
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant chunks using cosine similarity
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of relevant chunks with scores
        """
        try:
            if not self.is_fitted:
                logger.warning("TF-IDF index not fitted")
                return []
            
            logger.info(f"Searching for query: '{query[:50]}...' with top_k={top_k}")
            
            # Transform query to TF-IDF vector
            query_vector = self.vectorizer.transform([query])
            
            # Calculate cosine similarities
            similarities = cosine_similarity(query_vector, self.chunk_vectors).flatten()
            
            # Get top-k indices
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            # Prepare results
            results = []
            for idx in top_indices:
                if similarities[idx] > 0:  # Only include chunks with positive similarity
                    results.append({
                        'text': self.chunks[idx],
                        'score': float(similarities[idx]),
                        'index': int(idx)
                    })
            
            logger.info(f"Found {len(results)} relevant chunks")
            return results
            
        except Exception as e:
            logger.error(f"Error during search: {str(e)}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get index statistics"""
        if not self.is_fitted:
            return {"status": "not_fitted"}
        
        return {
            "status": "fitted",
            "num_chunks": len(self.chunks),
            "num_features": self.chunk_vectors.shape[1],
            "vectorizer_type": "TF-IDF"
        }
