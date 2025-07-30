"""
Basic text search service using simple string matching
No ML dependencies - guaranteed to work on any Python environment
"""
import logging
import re
from typing import List, Dict, Any, Optional
from collections import Counter

from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class BasicTextSearch:
    """
    Basic text search using simple string matching and keyword scoring
    No ML dependencies - uses only Python standard library
    """
    
    def __init__(self):
        self.chunks = []
        self.is_fitted = False
        
        logger.info("Initialized basic text search (no ML dependencies)")
    
    def create_index(self, chunks: List[str]) -> bool:
        """
        Create a simple text index from chunks
        
        Args:
            chunks: List of text chunks
            
        Returns:
            bool: True if successful
        """
        try:
            logger.info(f"Creating basic text index for {len(chunks)} chunks")
            
            self.chunks = chunks
            self.is_fitted = True
            
            logger.info(f"Basic text index created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error creating text index: {str(e)}")
            return False
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant chunks using simple text matching
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of relevant chunks with scores
        """
        try:
            if not self.is_fitted:
                logger.warning("Text index not created")
                return []
            
            logger.info(f"Searching for query: '{query[:50]}...' with top_k={top_k}")
            
            # Clean and tokenize query
            query_tokens = self._tokenize(query.lower())
            
            # Score each chunk
            chunk_scores = []
            for idx, chunk in enumerate(self.chunks):
                score = self._calculate_score(query_tokens, chunk.lower())
                if score > 0:
                    chunk_scores.append({
                        'text': chunk,
                        'score': score,
                        'index': idx
                    })
            
            # Sort by score and return top_k
            chunk_scores.sort(key=lambda x: x['score'], reverse=True)
            results = chunk_scores[:top_k]
            
            logger.info(f"Found {len(results)} relevant chunks")
            return results
            
        except Exception as e:
            logger.error(f"Error during search: {str(e)}")
            return []
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        # Remove punctuation and split into words
        text = re.sub(r'[^\w\s]', ' ', text)
        return [word for word in text.split() if len(word) > 2]
    
    def _calculate_score(self, query_tokens: List[str], chunk_text: str) -> float:
        """Calculate relevance score for a chunk"""
        chunk_tokens = self._tokenize(chunk_text)
        chunk_counter = Counter(chunk_tokens)
        
        score = 0.0
        total_query_words = len(query_tokens)
        
        for token in query_tokens:
            # Exact match
            if token in chunk_counter:
                score += chunk_counter[token] * 2.0
            
            # Partial match (contains token)
            elif any(token in chunk_token for chunk_token in chunk_tokens):
                score += 0.5
            
            # Fuzzy match (token contains part of query token)
            elif any(chunk_token in token for chunk_token in chunk_tokens):
                score += 0.3
        
        # Normalize by query length and chunk length
        if total_query_words > 0:
            score = score / total_query_words
        
        # Boost shorter chunks that are more focused
        if len(chunk_tokens) > 0:
            score = score * (1.0 + 1.0 / len(chunk_tokens))
        
        return score
    
    def get_stats(self) -> Dict[str, Any]:
        """Get index statistics"""
        if not self.is_fitted:
            return {"status": "not_fitted"}
        
        return {
            "status": "fitted",
            "num_chunks": len(self.chunks),
            "search_type": "basic_text_matching"
        }
