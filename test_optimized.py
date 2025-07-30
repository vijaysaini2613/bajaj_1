#!/usr/bin/env python3
"""
Quick test script to demonstrate the optimized PDF Q&A system
"""

import asyncio
import requests
import json

async def test_optimized_system():
    """Test the system with sample insurance content"""
    
    print("🚀 Testing Optimized Document Q&A System...")
    print("=" * 60)
    
    # Sample insurance policy text (more comprehensive)
    sample_policy = """
    COMPREHENSIVE AUTO INSURANCE POLICY
    Policy Number: AUTO-2024-789456
    
    SECTION I: LIABILITY COVERAGE
    A. Bodily Injury Liability: $250,000 per person, $500,000 per accident
    B. Property Damage Liability: $100,000 per accident
    C. Uninsured Motorist Coverage: $250,000 per person, $500,000 per accident
    
    SECTION II: PHYSICAL DAMAGE COVERAGE
    A. Comprehensive Coverage: $500 deductible
    B. Collision Coverage: $1,000 deductible
    C. Rental Reimbursement: $40 per day, maximum 30 days
    
    SECTION III: EXCLUSIONS
    This policy does not cover:
    1. Intentional damage or criminal acts
    2. Racing or speed contests
    3. Vehicles used for commercial delivery
    4. Damage from nuclear hazards
    5. War or military actions
    
    SECTION IV: PREMIUM AND POLICY PERIOD
    Annual Premium: $1,800
    Semi-annual Premium: $900
    Policy Period: January 1, 2024 to January 1, 2025
    
    SECTION V: CLAIMS PROCEDURE
    All claims must be reported within 72 hours of the incident.
    Contact our 24/7 claims hotline at 1-800-CLAIMS-1.
    A police report is required for all theft claims.
    """
    
    # Test questions
    test_questions = [
        "What is the bodily injury liability limit per person?",
        "What is the deductible for collision coverage?",
        "What exclusions apply to this policy?",
        "How much is the annual premium?",
        "What is the time limit for reporting claims?"
    ]
    
    print("📄 Sample Policy Loaded")
    print("❓ Test Questions:")
    for i, q in enumerate(test_questions, 1):
        print(f"   {i}. {q}")
    print()
    
    # Prepare request
    request_data = {
        "documents": [
            {
                "type": "text",
                "content": sample_policy
            }
        ],
        "questions": test_questions
    }
    
    try:
        print("🔄 Processing with optimized model...")
        response = requests.post(
            "http://127.0.0.1:8000/hackrx/run",
            json=request_data,
            headers={
                "Authorization": "Bearer your-secure-bearer-token-here",
                "Content-Type": "application/json"
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ SUCCESS! Answers Generated:")
            print("=" * 60)
            
            for i, answer in enumerate(result.get("answers", []), 1):
                print(f"\n{i}. Q: {answer['question']}")
                print(f"   A: {answer['answer']}")
                print(f"   📊 Confidence: {answer['confidence']*100:.1f}%")
                if answer.get('source_chunks'):
                    print(f"   📚 Source: {answer['source_chunks'][0][:100]}...")
            
            print(f"\n⚡ Processing Time: {result.get('processing_time', 'N/A')} seconds")
            print(f"🎯 Status: {result.get('status', 'Unknown')}")
            
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n💡 Make sure the server is running at http://127.0.0.1:8000")
        print("   Run: python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload")

if __name__ == "__main__":
    asyncio.run(test_optimized_system())
