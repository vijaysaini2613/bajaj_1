import os
import numpy as np
import faiss
from typing import List, Tuple
from sentence_transformers import SentenceTransformer

from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class VectorSearchService:
    """
    FAISS-based vector search service for semantic document retrieval
    """
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-mpnet-base-v2")
        self.model = None
        self.index = None
        self.chunks = []
        self.embeddings = None
        
        # Load the embedding model
        self._load_model()
    
    def _load_model(self):
        """Load the sentence transformer model"""
        try:
            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading embedding model: {str(e)}")
            raise
    
    def create_index(self, text_chunks: List[str]) -> None:
        """
        Create FAISS index from text chunks
        
        Args:
            text_chunks: List of text chunks to index
        """
        try:
            if not text_chunks:
                raise ValueError("No text chunks provided for indexing")
            
            logger.info(f"Creating FAISS index for {len(text_chunks)} chunks")
            
            # Store chunks
            self.chunks = text_chunks
            
            # Generate embeddings
            logger.info("Generating embeddings...")
            self.embeddings = self.model.encode(
                text_chunks,
                convert_to_numpy=True,
                show_progress_bar=True
            )
            
            # Create FAISS index
            dimension = self.embeddings.shape[1]
            logger.info(f"Creating FAISS index with dimension: {dimension}")
            
            # Use IndexFlatIP for cosine similarity (inner product after normalization)
            self.index = faiss.IndexFlatIP(dimension)
            
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(self.embeddings)
            
            # Add embeddings to index
            self.index.add(self.embeddings)
            
            logger.info(f"FAISS index created successfully with {self.index.ntotal} vectors")
            
        except Exception as e:
            logger.error(f"Error creating FAISS index: {str(e)}")
            raise
    
    def search(self, query: str, top_k: int = 5) -> List[str]:
        """
        Search for relevant text chunks using semantic similarity
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of relevant text chunks
        """
        try:
            if self.index is None:
                raise ValueError("Index not created. Call create_index() first.")
            
            if not query or not query.strip():
                raise ValueError("Query cannot be empty")
            
            logger.info(f"Searching for query: '{query[:50]}...' with top_k={top_k}")
            
            # Generate query embedding
            query_embedding = self.model.encode(
                [query.strip()],
                convert_to_numpy=True
            )
            
            # Normalize query embedding
            faiss.normalize_L2(query_embedding)
            
            # Search
            scores, indices = self.index.search(query_embedding, min(top_k, len(self.chunks)))
            
            # Extract relevant chunks
            relevant_chunks = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx >= 0 and idx < len(self.chunks):  # Valid index
                    chunk = self.chunks[idx]
                    relevant_chunks.append(chunk)
                    logger.debug(f"Result {i+1}: Score={score:.4f}, Chunk length={len(chunk)}")
            
            logger.info(f"Found {len(relevant_chunks)} relevant chunks")
            return relevant_chunks
            
        except Exception as e:
            logger.error(f"Error during search: {str(e)}")
            raise
    
    def search_with_scores(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Search for relevant text chunks with similarity scores
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of tuples (text_chunk, similarity_score)
        """
        try:
            if self.index is None:
                raise ValueError("Index not created. Call create_index() first.")
            
            if not query or not query.strip():
                raise ValueError("Query cannot be empty")
            
            logger.info(f"Searching for query with scores: '{query[:50]}...' with top_k={top_k}")
            
            # Generate query embedding
            query_embedding = self.model.encode(
                [query.strip()],
                convert_to_numpy=True
            )
            
            # Normalize query embedding
            faiss.normalize_L2(query_embedding)
            
            # Search
            scores, indices = self.index.search(query_embedding, min(top_k, len(self.chunks)))
            
            # Extract relevant chunks with scores
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx >= 0 and idx < len(self.chunks):  # Valid index
                    chunk = self.chunks[idx]
                    results.append((chunk, float(score)))
            
            logger.info(f"Found {len(results)} relevant chunks with scores")
            return results
            
        except Exception as e:
            logger.error(f"Error during search with scores: {str(e)}")
            raise
    
    def get_index_info(self) -> dict:
        """
        Get information about the current index
        
        Returns:
            Dictionary with index information
        """
        if self.index is None:
            return {"status": "not_created"}
        
        return {
            "status": "created",
            "total_vectors": self.index.ntotal,
            "dimension": self.index.d,
            "total_chunks": len(self.chunks),
            "model_name": self.model_name
        }
    
    def clear_index(self):
        """Clear the current index and chunks"""
        self.index = None
        self.chunks = []
        self.embeddings = None
        logger.info("Index cleared")
