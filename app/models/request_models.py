from pydantic import BaseModel, Field, validator
from typing import List, Literal
from enum import Enum

class DocumentType(str, Enum):
    """Supported document types"""
    PDF = "pdf"
    URL = "url"
    TEXT = "text"
    DOCX = "docx"

class DocumentInput(BaseModel):
    """Input document model"""
    type: DocumentType = Field(..., description="Type of document (pdf, url, text, docx)")
    content: str = Field(..., description="Document content or URL")
    
    @validator('content')
    def validate_content(cls, v, values):
        """Validate content based on document type"""
        if not v or not v.strip():
            raise ValueError("Content cannot be empty")
        
        doc_type = values.get('type')
        if doc_type == DocumentType.URL:
            if not (v.startswith('http://') or v.startswith('https://')):
                raise ValueError("URL must start with http:// or https://")
        
        return v.strip()

class DocumentQARequest(BaseModel):
    """Request model for document Q&A"""
    documents: List[DocumentInput] = Field(..., min_items=1, description="List of documents to process")
    questions: List[str] = Field(..., min_items=1, description="List of questions to answer")
    
    @validator('questions')
    def validate_questions(cls, v):
        """Validate questions are not empty"""
        if not v:
            raise ValueError("At least one question is required")
        
        validated_questions = []
        for question in v:
            if not question or not question.strip():
                raise ValueError("Questions cannot be empty")
            validated_questions.append(question.strip())
        
        return validated_questions

    class Config:
        json_schema_extra = {
            "example": {
                "documents": [
                    {
                        "type": "url",
                        "content": "https://example.com/policy.pdf"
                    },
                    {
                        "type": "text",
                        "content": "Your insurance policy document text here..."
                    }
                ],
                "questions": [
                    "What is the coverage limit for medical expenses?",
                    "What are the exclusions in this policy?"
                ]
            }
        }
