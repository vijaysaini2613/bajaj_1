from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime

class AnswerResult(BaseModel):
    """Individual answer result"""
    question: str = Field(..., description="The original question")
    answer: str = Field(..., description="The extracted answer from the document")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score for the answer")
    source_chunks: List[str] = Field(default=[], description="Source text chunks used for the answer")
    reasoning: Optional[str] = Field(None, description="Optional reasoning for the answer")

class DocumentQAResponse(BaseModel):
    """Response model for document Q&A"""
    answers: List[AnswerResult] = Field(..., description="List of answers for each question")
    processing_time: float = Field(..., description="Total processing time in seconds")
    status: str = Field(..., description="Processing status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    metadata: Optional[dict] = Field(default=None, description="Additional metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "answers": [
                    {
                        "question": "What is the coverage limit for medical expenses?",
                        "answer": "The coverage limit for medical expenses is $100,000 per incident as specified in Section 3.2.1.",
                        "confidence": 0.95,
                        "source_chunks": [
                            "Section 3.2.1: Medical expense coverage shall not exceed $100,000 per incident..."
                        ],
                        "reasoning": "Found explicit coverage limit in Section 3.2.1"
                    }
                ],
                "processing_time": 2.3,
                "status": "success",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")
    status_code: int = Field(..., description="HTTP status code")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid document format",
                "detail": "Unable to process the provided PDF file",
                "timestamp": "2024-01-01T12:00:00Z",
                "status_code": 400
            }
        }
