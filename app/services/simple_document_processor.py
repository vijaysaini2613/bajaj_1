import asyncio
import pypdf
import io
import os
from typing import List, Dict, Any
from urllib.parse import urljoin, urlparse

class SimpleDocumentProcessor:
    """
    Minimal document processor without Pydantic dependencies
    """
    
    def __init__(self):
        self.supported_extensions = {
            'pdf': self._process_pdf,
            'txt': self._process_text
        }
    
    async def process_document(self, doc_type: str, content: str, filename: str = "") -> List[str]:
        """
        Process a document and return extracted text chunks
        
        Args:
            doc_type: Type of document ('pdf', 'text', 'url')
            content: Document content (base64 for files, URL for web, text for text)
            filename: Optional filename for context
            
        Returns:
            List of text chunks extracted from the document
        """
        try:
            if doc_type == "pdf":
                return await self._process_pdf(content)
            elif doc_type == "text":
                return await self._process_text(content)
            elif doc_type == "url":
                return await self._process_url(content)
            else:
                raise ValueError(f"Unsupported document type: {doc_type}")
                
        except Exception as e:
            print(f"Error processing document: {str(e)}")
            # Return the content as-is if processing fails
            return [content[:5000]] if content else ["No content available"]
    
    async def _process_pdf(self, base64_content: str) -> List[str]:
        """Process PDF content from base64 string"""
        try:
            import base64
            # Decode base64 content
            pdf_bytes = base64.b64decode(base64_content)
            
            # Create PDF reader
            pdf_file = io.BytesIO(pdf_bytes)
            pdf_reader = pypdf.PdfReader(pdf_file)
            
            chunks = []
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    text = page.extract_text()
                    if text.strip():
                        # Split large pages into smaller chunks
                        page_chunks = self._split_text_into_chunks(text, max_length=2000)
                        for i, chunk in enumerate(page_chunks):
                            chunks.append(f"Page {page_num + 1}, Part {i + 1}: {chunk}")
                except Exception as e:
                    print(f"Error extracting text from page {page_num + 1}: {str(e)}")
                    continue
            
            return chunks if chunks else ["No text could be extracted from the PDF"]
            
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return ["Error processing PDF file"]
    
    async def _process_text(self, text_content: str) -> List[str]:
        """Process plain text content"""
        if not text_content.strip():
            return ["No content provided"]
        
        # Split into manageable chunks
        chunks = self._split_text_into_chunks(text_content, max_length=2000)
        return chunks
    
    async def _process_url(self, url: str) -> List[str]:
        """Process content from URL - simplified version"""
        try:
            # For minimal version, just return a placeholder
            return [f"URL processing not available in minimal mode: {url}"]
        except Exception as e:
            print(f"Error processing URL: {str(e)}")
            return ["Error processing URL"]
    
    def _split_text_into_chunks(self, text: str, max_length: int = 2000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + max_length
            
            # If we're not at the end, try to break at a sentence or paragraph
            if end < len(text):
                # Look for sentence endings
                for punct in ['. ', '.\n', '!\n', '?\n']:
                    last_punct = text.rfind(punct, start, end)
                    if last_punct > start + max_length // 2:
                        end = last_punct + 1
                        break
                else:
                    # Look for word boundaries
                    last_space = text.rfind(' ', start, end)
                    if last_space > start + max_length // 2:
                        end = last_space
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start forward with overlap
            start = max(end - overlap, start + 1)
            if start >= len(text):
                break
        
        return chunks

    def _clean_text(self, text: str) -> str:
        """Basic text cleaning"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Remove special characters but keep basic punctuation
        import re
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', ' ', text)
        
        return text.strip()
