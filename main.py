from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
import logging
from dotenv import load_dotenv

from app.models.request_models import DocumentQARequest
from app.models.response_models import DocumentQAResponse
from app.services.document_processor import DocumentProcessor

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

from app.services.llm_service import LLMService
from app.utils.logger import setup_logger

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Document Q&A System",
    description="AI-powered document analysis and Q&A system for insurance policies and legal documents",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Security
security = HTTPBearer()
BEARER_TOKEN = os.getenv("BEARER_TOKEN", "default_token")

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify bearer token authentication"""
    if credentials.credentials != BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return credentials.credentials

# Initialize services
document_processor = DocumentProcessor()
vector_search = VectorSearchService()
llm_service = LLMService()

# Log which vector search implementation is being used
logger.info(f"Using {VECTOR_SEARCH_TYPE} vector search implementation")

@app.get("/")
async def root():
    """Serve the main web interface"""
    return FileResponse('static/index.html')

@app.get("/health")
async def health_check():
    """Detailed health check"""
    try:
        # Check if services are properly initialized
        services_status = {
            "document_processor": "healthy" if document_processor else "unhealthy",
            "vector_search": "healthy" if vector_search else "unhealthy",
            "llm_service": "healthy" if llm_service else "unhealthy",
        }
        
        return {
            "status": "healthy",
            "services": services_status,
            "vector_search_type": VECTOR_SEARCH_TYPE,
            "environment": os.getenv("ENVIRONMENT", "development")
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Service unhealthy")

@app.post("/hackrx/run", response_model=DocumentQAResponse)
async def process_documents_and_answer(
    request: DocumentQARequest,
    token: str = Depends(verify_token)
):
    """
    Main endpoint for document Q&A processing
    
    This endpoint:
    1. Processes multiple document types (PDF, URL, text)
    2. Creates vector embeddings using sentence transformers
    3. Performs semantic search with FAISS
    4. Uses GPT-4 with specialized prompts for accurate answers
    5. Returns structured JSON responses
    """
    try:
        logger.info(f"Processing request with {len(request.documents)} documents and {len(request.questions)} questions")
        
        # Step 1: Process all documents
        all_chunks = []
        for doc in request.documents:
            logger.info(f"Processing document of type: {doc.type}")
            chunks = await document_processor.process_document(doc)
            all_chunks.extend(chunks)
        
        if not all_chunks:
            raise HTTPException(status_code=400, detail="No content could be extracted from the provided documents")
        
        logger.info(f"Extracted {len(all_chunks)} text chunks from documents")
        
        # Step 2: Create vector index
        vector_search.create_index(all_chunks)
        logger.info("Created FAISS vector index")
        
        # Step 3: Process each question
        answers = []
        for question in request.questions:
            logger.info(f"Processing question: {question[:50]}...")
            
            # Search for relevant context
            relevant_chunks = vector_search.search(question, top_k=5)
            context = "\n\n".join(relevant_chunks)
            
            # Generate answer using LLM
            answer_data = await llm_service.generate_answer(question, context)
            answers.append(answer_data)
        
        logger.info(f"Successfully processed all {len(request.questions)} questions")
        
        return DocumentQAResponse(
            answers=answers,
            processing_time=0.0,  # Will be calculated in middleware
            status="success"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("ENVIRONMENT") == "development",
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )
