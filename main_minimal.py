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
    # For web interface requests, skip authentication
    user_agent = request.headers.get("user-agent", "").lower()
    if "mozilla" in user_agent or "chrome" in user_agent or "safari" in user_agent:
        return True
    
    # For API requests, require authentication
    auth_header = request.headers.get("authorization", "")
    if not auth_header.startswith("Bearer "):
        return False
    token = auth_header.replace("Bearer ", "")
    return token == BEARER_TOKEN

# Initialize services (LLM service will be initialized on first use)
document_processor = SimpleDocumentProcessor()
vector_search = VectorSearchService()
llm_service = None  # Will be initialized when needed

# Log which vector search implementation is being used
print(f"Using {VECTOR_SEARCH_TYPE} vector search implementation")

def get_llm_service():
    """Lazy initialization of LLM service"""
    global llm_service
    if llm_service is None:
        try:
            print("Initializing LLM service...")
            llm_service = LLMService()
            print("LLM service initialized successfully")
        except Exception as e:
            print(f"Error initializing LLM service: {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail=f"LLM service not available: {str(e)}. Please check GEMINI_API_KEY environment variable."
            )
    return llm_service

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

@app.get("/debug/env")
async def debug_env():
    """Debug endpoint to check environment variables (remove in production)"""
    return {
        "has_gemini_key": "GEMINI_API_KEY" in os.environ,
        "gemini_key_length": len(os.getenv("GEMINI_API_KEY", "")) if os.getenv("GEMINI_API_KEY") else 0,
        "has_bearer_token": "BEARER_TOKEN" in os.environ,
        "environment": os.getenv("ENVIRONMENT", "development"),
        "available_env_vars": [key for key in os.environ.keys() if not key.startswith("_")]
    }

@app.post("/hackrx/run")
async def process_documents_and_answer(request: Request):
    """
    Main endpoint for document Q&A processing
    Simplified version without Pydantic validation
    """
    try:
        print("=== Starting request processing ===")
        
        # Simple authentication
        if not verify_token(request):
            print("Authentication failed")
            raise HTTPException(status_code=403, detail="Not authenticated")
        
        print("Authentication successful")
        
        # Parse request manually
        try:
            body = await request.json()
            print(f"Request body received: {str(body)[:200]}...")
        except Exception as e:
            print(f"Failed to parse JSON: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
        
        try:
            qa_request = SimpleDocumentQARequest(body)
            print("Request object created successfully")
        except Exception as e:
            print(f"Failed to create request object: {str(e)}")
            raise HTTPException(status_code=422, detail=f"Request validation failed: {str(e)}")
        
        start_time = time.time()
        
        print(f"Processing request with {len(qa_request.documents)} documents and {len(qa_request.questions)} questions")
        
        # Process documents and extract text
        all_chunks = []
        try:
            for doc in qa_request.documents:
                print(f"Processing document of type: {doc.type}")
                try:
                    chunks = await document_processor.process_document(doc.type, doc.content, doc.filename)
                    all_chunks.extend(chunks)
                    print(f"Successfully processed document: {len(chunks)} chunks")
                except Exception as e:
                    print(f"Error processing document: {str(e)}")
                    raise HTTPException(status_code=400, detail=f"Document processing failed: {str(e)}")
        except HTTPException:
            raise
        except Exception as e:
            print(f"Unexpected error in document processing: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Document processing error: {str(e)}")
        
        print(f"Extracted {len(all_chunks)} text chunks from documents")
        
        # Create vector index
        try:
            vector_search.create_index(all_chunks)
            print("Created vector index")
        except Exception as e:
            print(f"Error creating vector index: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Vector index creation failed: {str(e)}")
        
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
                llm = get_llm_service()  # Lazy initialization
                answer_result = await llm.generate_answer(question, context_text)
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
        try:
            response = SimpleDocumentQAResponse(answers, processing_time)
            response_dict = response.to_dict()
            print("Response created successfully")
            return JSONResponse(content=response_dict)
        except Exception as e:
            print(f"Error creating response: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Response creation failed: {str(e)}")
        
    except ValueError as e:
        print(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
