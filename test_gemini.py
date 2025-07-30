#!/usr/bin/env python3
"""
Quick test to verify Gemini API is working
"""
import requests
import json

def test_single_question():
    """Test a single question to verify the system is working"""
    
    url = "http://127.0.0.1:8000/hackrx/run"
    
    # Test data with both document and questions
    test_data = {
        "documents": [
            {
                "type": "PDF",
                "content": "ArogyaSanjeevaniPolicy-SampleDocument.pdf",
                "filename": "ArogyaSanjeevaniPolicy-SampleDocument.pdf"
            }
        ],
        "questions": ["What is the sum insured under this policy?"]
    }
    
    # Add Bearer token for authentication
    headers = {
        "Authorization": "Bearer your-secure-bearer-token-here",
        "Content-Type": "application/json"
    }
    
    print("🧪 Testing Gemini API with a simple question...")
    print(f"Question: {test_data['questions'][0]}")
    print("=" * 60)
    
    try:
        response = requests.post(url, json=test_data, headers=headers, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            answer = result['answers'][0]
            
            print(f"✅ SUCCESS!")
            print(f"Answer: {answer['answer']}")
            print(f"Confidence: {answer['confidence']:.1%}")
            print(f"Sources: {len(answer['sources'])} chunks used")
            
            if answer['confidence'] > 0.5:
                print("🎉 System is working well!")
            else:
                print("⚠️ Low confidence - may need tuning")
                
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        print("Make sure the server is running on http://127.0.0.1:8000")

if __name__ == "__main__":
    test_single_question()
