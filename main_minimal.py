"""
Minimal FastAPI application without Pydantic dependencies
For ultra-minimal deployment on restricted environments
"""
import os
import time
import json
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Import our services and models
from app.services.simple_document_processor import SimpleDocumentProcessor
from app.services.llm_service import LLMService
from app.models.simple_models import (
    SimpleDocumentQARequest, 
    SimpleDocumentQAResponse, 
    SimpleAnswerResult
)

# Try to import vector search services with fallbacks
try:
    from app.services.vector_search import VectorSearchService
    VECTOR_SEARCH_TYPE = "FAISS"
except ImportError:
    try:
        from app.services.lightweight_vector_search import LightweightVectorSearch as VectorSearchService
        VECTOR_SEARCH_TYPE = "Lightweight"
    except ImportError:
        from app.services.basic_text_search import BasicTextSearch as VectorSearchService
        VECTOR_SEARCH_TYPE = "Basic"

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Document Q&A System",
    description="AI-powered document analysis with Google Gemini",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Simple authentication
BEARER_TOKEN = os.getenv("BEARER_TOKEN", "default_token")

def verify_token(request: Request) -> bool:
    """Simple token verification without dependencies"""
    auth_header = request.headers.get("authorization", "")
    if not auth_header.startswith("Bearer "):
        return False
    token = auth_header.replace("Bearer ", "")
    return token == BEARER_TOKEN

# Initialize services
document_processor = SimpleDocumentProcessor()
vector_search = VectorSearchService()
llm_service = LLMService()

# Log which vector search implementation is being used
print(f"Using {VECTOR_SEARCH_TYPE} vector search implementation")

@app.get("/")
async def root():
    """Serve the main web interface"""
    return FileResponse('static/index.html')

@app.get("/health")
async def health_check():
    """Simple health check"""
    return {
        "status": "healthy",
        "vector_search_type": VECTOR_SEARCH_TYPE,
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.post("/hackrx/run")
async def process_documents_and_answer(request: Request):
    """
    Main endpoint for document Q&A processing
    Simplified version without Pydantic validation
    """
    try:
        # Simple authentication
        if not verify_token(request):
            raise HTTPException(status_code=403, detail="Not authenticated")
        
        # Parse request manually
        body = await request.json()
        qa_request = SimpleDocumentQARequest(body)
        
        start_time = time.time()
        
        print(f"Processing request with {len(qa_request.documents)} documents and {len(qa_request.questions)} questions")
        
        # Process documents and extract text
        all_chunks = []
        for doc in qa_request.documents:
            print(f"Processing document of type: {doc.type}")
            chunks = await document_processor.process_document(doc.type, doc.content, doc.filename)
            all_chunks.extend(chunks)
        
        print(f"Extracted {len(all_chunks)} text chunks from documents")
        
        # Create vector index
        vector_search.create_index(all_chunks)
        print("Created vector index")
        
        # Process each question
        answers = []
        for question in qa_request.questions:
            print(f"Processing question: {question[:50]}...")
            
            # Search for relevant chunks
            relevant_chunks = vector_search.search(question, top_k=5)
            print(f"Found {len(relevant_chunks)} relevant chunks")
            
            # Generate answer using LLM
            context_text = "\n\n".join([chunk.get('text', chunk) for chunk in relevant_chunks])
            
            try:
                answer_result = await llm_service.generate_answer(question, context_text)
                source_texts = [chunk.get('text', chunk)[:200] + "..." for chunk in relevant_chunks[:3]]
                
                answers.append(SimpleAnswerResult(
                    question=question,
                    answer=answer_result.answer,
                    confidence=answer_result.confidence,
                    sources=source_texts
                ))
            except Exception as e:
                print(f"Error generating answer: {str(e)}")
                answers.append(SimpleAnswerResult(
                    question=question,
                    answer="An error occurred while processing this question. Please try again.",
                    confidence=0.0,
                    sources=[]
                ))
        
        processing_time = time.time() - start_time
        print(f"Successfully processed all {len(qa_request.questions)} questions")
        
        # Create response
        response = SimpleDocumentQAResponse(answers, processing_time)
        return JSONResponse(content=response.to_dict())
        
    except ValueError as e:
        print(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
