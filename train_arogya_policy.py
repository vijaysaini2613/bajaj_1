#!/usr/bin/env python3
"""
Train the Document Q&A system with Arogya Sanjeevani Policy
"""

import asyncio
import base64
import json
from pathlib import Path

async def train_with_arogya_policy():
    """Train the system with the Arogya Sanjeevani Policy PDF"""
    
    print("🏥 Training Document Q&A System with Arogya Sanjeevani Policy")
    print("=" * 70)
    
    # Path to the PDF
    pdf_path = Path("arogya_policy.pdf")
    
    if not pdf_path.exists():
        print("❌ PDF file not found. Please ensure 'arogya_policy.pdf' is in the project directory.")
        return False
    
    try:
        # Read and encode PDF
        print("📄 Reading PDF file...")
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
            pdf_base64 = base64.b64encode(pdf_data).decode()
        
        print(f"✅ PDF loaded: {len(pdf_data)} bytes")
        
        # Prepare comprehensive questions for insurance policy
        insurance_questions = [
            # Coverage Questions
            "What is the sum insured under this policy?",
            "What are the coverage benefits provided?",
            "What is covered under hospitalization?",
            "What are the pre-hospitalization expenses covered?",
            "What are the post-hospitalization expenses covered?",
            
            # Exclusions
            "What are the general exclusions in this policy?",
            "What medical conditions are not covered?",
            "Are pre-existing diseases covered?",
            "What treatments are excluded from coverage?",
            
            # Policy Terms
            "What is the policy period?",
            "What is the waiting period for coverage?",
            "What is the waiting period for pre-existing diseases?",
            "What is the room rent limit?",
            "What is the ICU room rent limit?",
            
            # Claims Process
            "What is the claim settlement process?",
            "What documents are required for claims?",
            "What is the cashless facility procedure?",
            "What is the reimbursement claim procedure?",
            "What is the claim intimation time limit?",
            
            # Premium and Renewal
            "How is the premium calculated?",
            "What are the renewal conditions?",
            "Is there a grace period for premium payment?",
            "What happens if premium is not paid on time?",
            
            # Additional Benefits
            "What additional benefits are provided?",
            "Is ambulance service covered?",
            "Are health check-ups covered?",
            "Is home nursing covered?",
            "What is the ayush treatment coverage?"
        ]
        
        print(f"📝 Prepared {len(insurance_questions)} specialized questions")
        
        # Create request payload
        request_data = {
            "documents": [
                {
                    "type": "pdf",
                    "content": pdf_base64
                }
            ],
            "questions": insurance_questions
        }
        
        print("🔄 Processing document and generating training embeddings...")
        print("   This may take a few minutes for the first time...")
        
        # Import requests here to make the call
        import requests
        
        response = requests.post(
            "http://127.0.0.1:8000/hackrx/run",
            json=request_data,
            headers={
                "Authorization": "Bearer your-secure-bearer-token-here",
                "Content-Type": "application/json"
            },
            timeout=300  # 5 minutes timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ TRAINING COMPLETED SUCCESSFULLY!")
            print("=" * 70)
            print(f"📊 Processed {len(result.get('answers', []))} questions")
            print(f"⚡ Processing time: {result.get('processing_time', 'N/A')} seconds")
            
            # Show sample results
            print("\n🎯 Sample Trained Responses:")
            print("-" * 50)
            
            for i, answer in enumerate(result.get("answers", [])[:5], 1):
                confidence_color = "🟢" if answer['confidence'] > 0.8 else "🟡" if answer['confidence'] > 0.5 else "🔴"
                print(f"\n{i}. Q: {answer['question']}")
                print(f"   A: {answer['answer'][:100]}{'...' if len(answer['answer']) > 100 else ''}")
                print(f"   {confidence_color} Confidence: {answer['confidence']*100:.1f}%")
            
            # Save training results
            with open("training_results.json", "w") as f:
                json.dump(result, f, indent=2)
            
            print(f"\n💾 Training results saved to 'training_results.json'")
            print("\n🎉 Your system is now trained on the Arogya Sanjeevani Policy!")
            print("\n📚 You can now ask questions like:")
            print("   • 'What is the sum insured?'")
            print("   • 'What are the exclusions?'")
            print("   • 'What is the waiting period?'")
            print("   • 'How do I file a claim?'")
            
            return True
            
        else:
            print(f"❌ Training failed: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during training: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(train_with_arogya_policy())
    if success:
        print("\n🚀 Ready to answer questions about Arogya Sanjeevani Policy!")
    else:
        print("\n💡 Make sure the server is running: python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload")
