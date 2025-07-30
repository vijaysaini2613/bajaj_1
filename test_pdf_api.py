#!/usr/bin/env python3
"""
Test Gemini API with actual PDF file
"""
import requests
import json
import base64

def test_with_pdf():
    """Test with the actual PDF file"""
    
    url = "http://127.0.0.1:8000/hackrx/run"
    
    # Read the PDF file and encode it as base64
    try:
        with open("arogya_policy.pdf", "rb") as f:
            pdf_content = base64.b64encode(f.read()).decode('utf-8')
    except FileNotFoundError:
        print("❌ PDF file not found. Make sure 'arogya_policy.pdf' exists in the current directory.")
        return
    
    # Test data with PDF content
    test_data = {
        "documents": [
            {
                "type": "pdf",
                "content": pdf_content,
                "filename": "arogya_policy.pdf"
            }
        ],
        "questions": ["What is the sum insured under this policy?"]
    }
    
    # Add Bearer token for authentication
    headers = {
        "Authorization": "Bearer your-secure-bearer-token-here",
        "Content-Type": "application/json"
    }
    
    print("🧪 Testing Gemini API with PDF document...")
    print(f"📄 PDF size: {len(pdf_content)} characters (base64)")
    print(f"❓ Question: {test_data['questions'][0]}")
    print("=" * 60)
    
    try:
        print("🔄 Sending request...")
        response = requests.post(url, json=test_data, headers=headers, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            answer = result['answers'][0]
            
            print(f"✅ SUCCESS!")
            print(f"📝 Answer: {answer['answer']}")
            print(f"🎯 Confidence: {answer['confidence']:.1%}")
            
            # Handle sources field safely
            sources_count = 0
            if 'sources' in answer and answer['sources']:
                sources_count = len(answer['sources'])
            print(f"📚 Sources: {sources_count} chunks used")
            
            if answer['confidence'] > 0.7:
                print("🎉 High confidence - System is working excellently!")
            elif answer['confidence'] > 0.5:
                print("✅ Good confidence - System is working well!")
            else:
                print("⚠️ Low confidence - Answer may need verification")
                
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_with_pdf()
