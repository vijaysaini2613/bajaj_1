import re
import os
from typing import List
from urllib.parse import urlparse

def clean_text(text: str) -> str:
    """
    Clean and normalize text content
    
    Args:
        text: Raw text to clean
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace and normalize line breaks
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # Remove special characters but keep punctuation
    # text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\"\'\/]', '', text)
    
    return text

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> List[str]:
    """
    Split text into overlapping chunks optimized for insurance/legal documents
    
    Args:
        text: Text to chunk
        chunk_size: Maximum size of each chunk (smaller for better accuracy)
        overlap: Number of characters to overlap between chunks
        
    Returns:
        List of text chunks
    """
    if not text:
        return []
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Try to end at a sentence boundary for better semantic coherence
        if end < len(text):
            # Look for sentence endings within the last 150 characters
            sentence_end = text.rfind('.', end - 150, end)
            if sentence_end > start:
                end = sentence_end + 1
            else:
                # If no sentence boundary, try paragraph break
                para_end = text.rfind('\n\n', end - 150, end)
                if para_end > start:
                    end = para_end + 2
        
        chunk = text[start:end].strip()
        if chunk and len(chunk) > 50:  # Only keep meaningful chunks
            chunks.append(chunk)
        
        start = end - overlap
        
        # Prevent infinite loop
        if start >= end:
            break
    
    return chunks

def extract_clauses(text: str) -> List[str]:
    """
    Extract clauses from legal/insurance document text
    
    Args:
        text: Document text
        
    Returns:
        List of extracted clauses
    """
    # Pattern to identify section headers and clauses
    section_patterns = [
        r'\b(?:Section|Article|Clause|Paragraph)\s+\d+[\.\d]*\s*:?\s*([^\n]+)',
        r'\b\d+[\.\d]*\s+([A-Z][^\n]+)',
        r'\b[A-Z]\.\s+([^\n]+)',
    ]
    
    clauses = []
    
    for pattern in section_patterns:
        matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
        for match in matches:
            clause = match.group(0).strip()
            if len(clause) > 20:  # Filter out very short matches
                clauses.append(clause)
    
    # Also chunk the text normally
    text_chunks = chunk_text(text)
    clauses.extend(text_chunks)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_clauses = []
    for clause in clauses:
        if clause not in seen:
            seen.add(clause)
            unique_clauses.append(clause)
    
    return unique_clauses

def validate_url(url: str) -> bool:
    """
    Validate if a string is a valid URL
    
    Args:
        url: URL string to validate
        
    Returns:
        True if valid URL, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def get_file_extension(filename: str) -> str:
    """
    Get file extension from filename
    
    Args:
        filename: Name of the file
        
    Returns:
        File extension (without dot)
    """
    return os.path.splitext(filename)[1].lower().lstrip('.')

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe storage
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove special characters and replace with underscore
    filename = re.sub(r'[^\w\s\-\.]', '_', filename)
    # Remove extra underscores and spaces
    filename = re.sub(r'[_\s]+', '_', filename)
    return filename.strip('_')
