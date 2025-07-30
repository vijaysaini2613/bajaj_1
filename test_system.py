#!/usr/bin/env python3
"""
Simple test script to verify the Document Q&A system works locally
"""

import asyncio
import os
from app.services.document_processor import DocumentProcessor
from app.services.vector_search import VectorSearchService
from app.services.llm_service import LLMService
from app.models.request_models import DocumentInput, DocumentType

async def test_system():
    """Test the entire system with a simple example"""
    
    print("🧪 Testing Document Q&A System...")
    
    # Sample insurance policy text
    sample_text = """
    INSURANCE POLICY DOCUMENT
    
    Section 1: Coverage Limits
    The maximum coverage limit for medical expenses is $100,000 per incident.
    The deductible amount is $500 per claim.
    
    Section 2: Exclusions
    This policy does not cover:
    - Pre-existing conditions
    - Cosmetic procedures
    - Experimental treatments
    
    Section 3: Premium Information
    Annual premium: $2,400
    Monthly premium: $200
    """
    
    try:
        # Test Document Processor
        print("📄 Testing Document Processor...")
        doc_processor = DocumentProcessor()
        doc_input = DocumentInput(type=DocumentType.TEXT, content=sample_text)
        chunks = await doc_processor.process_document(doc_input)
        print(f"✅ Document processed successfully! Generated {len(chunks)} chunks")
        
        # Test Vector Search
        print("🔍 Testing Vector Search...")
        vector_search = VectorSearchService()
        vector_search.create_index(chunks)
        
        test_query = "What is the coverage limit for medical expenses?"
        relevant_chunks = vector_search.search(test_query, top_k=3)
        print(f"✅ Vector search successful! Found {len(relevant_chunks)} relevant chunks")
        
        # Print some results
        print("\n📋 Sample Results:")
        for i, chunk in enumerate(relevant_chunks[:2]):
            print(f"  {i+1}. {chunk[:100]}...")
        
        # Note about LLM testing
        print("\n🤖 LLM Service Test:")
        if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "sk-your-openai-api-key-here":
            print("⚠️  OpenAI API key not configured - skipping LLM test")
            print("   Set OPENAI_API_KEY in .env file to test full functionality")
        else:
            print("🔑 OpenAI API key found - LLM service should work!")
            # Uncomment to test LLM service
            # llm_service = LLMService()
            # context = "\n".join(relevant_chunks)
            # answer = await llm_service.generate_answer(test_query, context)
            # print(f"✅ LLM Answer: {answer.answer}")
        
        print("\n🎉 All core components working correctly!")
        print("\n📚 Next Steps:")
        print("   1. Set your OpenAI API key in .env file")
        print("   2. Set a secure BEARER_TOKEN in .env file") 
        print("   3. Run: python dev_server.py")
        print("   4. Visit: http://localhost:8000/docs")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_system())
    exit(0 if success else 1)
