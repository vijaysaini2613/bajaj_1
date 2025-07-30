#!/usr/bin/env python3
"""
Comprehensive test of the Document Q&A system with multiple questions
"""
import requests
import json
import base64

def test_multiple_questions():
    """Test multiple insurance-related questions"""
    
    url = "http://127.0.0.1:8000/hackrx/run"
    
    # Read the PDF file and encode it as base64
    with open("arogya_policy.pdf", "rb") as f:
        pdf_content = base64.b64encode(f.read()).decode('utf-8')
    
    # Test with multiple questions about the insurance policy
    questions = [
        "What is the sum insured under this policy?",
        "What are the main exclusions?",
        "What is the waiting period for pre-existing diseases?",
        "What expenses are covered under hospitalization?",
        "How do I file a claim?"
    ]
    
    test_data = {
        "documents": [
            {
                "type": "pdf",
                "content": pdf_content,
                "filename": "arogya_policy.pdf"
            }
        ],
        "questions": questions
    }
    
    headers = {
        "Authorization": "Bearer your-secure-bearer-token-here",
        "Content-Type": "application/json"
    }
    
    print("🏥 COMPREHENSIVE INSURANCE POLICY Q&A TEST")
    print("=" * 70)
    print(f"📄 Testing with {len(questions)} questions")
    print("🔄 Processing...")
    print()
    
    try:
        response = requests.post(url, json=test_data, headers=headers, timeout=180)
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ ALL QUESTIONS PROCESSED SUCCESSFULLY!")
            print("=" * 70)
            
            for i, answer in enumerate(result['answers'], 1):
                print(f"\n🔹 QUESTION {i}: {questions[i-1]}")
                print(f"📝 ANSWER: {answer['answer']}")
                print(f"🎯 CONFIDENCE: {answer['confidence']:.1%}")
                
                if answer['confidence'] >= 0.8:
                    print("✅ EXCELLENT")
                elif answer['confidence'] >= 0.6:
                    print("✅ GOOD")
                else:
                    print("⚠️ NEEDS REVIEW")
                    
                print("-" * 50)
            
            # Calculate average confidence
            avg_confidence = sum(ans['confidence'] for ans in result['answers']) / len(result['answers'])
            print(f"\n📊 OVERALL PERFORMANCE:")
            print(f"🎯 Average Confidence: {avg_confidence:.1%}")
            
            if avg_confidence >= 0.8:
                print("🎉 EXCELLENT - System is working exceptionally well!")
            elif avg_confidence >= 0.6:
                print("✅ GOOD - System is performing well!")
            else:
                print("⚠️ FAIR - System may need tuning for better accuracy")
                
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_multiple_questions()
