"""
Simple request/response models without Pydantic
For ultra-minimal deployment compatibility
"""
from typing import List, Dict, Any, Optional

class SimpleDocumentInput:
    """Simple document input without Pydantic validation"""
    
    def __init__(self, data: dict):
        self.type = data.get('type', '').lower()
        self.content = data.get('content', '')
        self.filename = data.get('filename', 'unknown')
        
        # Basic validation
        if not self.type or self.type not in ['pdf', 'url', 'text', 'docx']:
            raise ValueError(f"Invalid document type: {self.type}")
        if not self.content:
            raise ValueError("Document content is required")

class SimpleDocumentQARequest:
    """Simple document Q&A request without Pydantic"""
    
    def __init__(self, data: dict):
        self.documents = []
        self.questions = []
        
        # Parse documents
        docs_data = data.get('documents', [])
        if not docs_data:
            raise ValueError("At least one document is required")
        
        for doc_data in docs_data:
            self.documents.append(SimpleDocumentInput(doc_data))
        
        # Parse questions
        questions_data = data.get('questions', [])
        if not questions_data:
            raise ValueError("At least one question is required")
        
        for question in questions_data:
            if not question or not question.strip():
                raise ValueError("Questions cannot be empty")
            self.questions.append(question.strip())

class SimpleAnswerResult:
    """Simple answer result without Pydantic"""
    
    def __init__(self, question: str, answer: str, confidence: float, sources: List[str] = None):
        self.question = question
        self.answer = answer
        self.confidence = confidence
        self.sources = sources or []
    
    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "answer": self.answer,
            "confidence": self.confidence,
            "sources": self.sources
        }

class SimpleDocumentQAResponse:
    """Simple document Q&A response without Pydantic"""
    
    def __init__(self, answers: List[SimpleAnswerResult], processing_time: float):
        self.answers = answers
        self.processing_time = processing_time
    
    def to_dict(self) -> dict:
        return {
            "answers": [answer.to_dict() for answer in self.answers],
            "processing_time": self.processing_time,
            "total_questions": len(self.answers)
        }
