# Document Q&A System with FastAPI and FAISS

A production-ready document Q&A system that processes insurance policies, legal documents, and other text sources to provide accurate, contextual answers using LLM technology.

## 🚀 Features

- **FastAPI Backend** with `/hackrx/run` endpoint
- **FAISS Vector Search** for semantic document retrieval
- **OpenAI GPT-4 Integration** with specialized prompting for insurance/legal documents
- **Multi-format Support**: PDF, DOCX, URLs, and plain text
- **Bearer Token Authentication** for secure API access
- **Deployment Ready** for Render hosting
- **Comprehensive Logging** and error handling

## 🏗️ Architecture

```
[User POST /hackrx/run] → [FastAPI Backend] → [PDF/URL Loader] → [Text Splitter]
→ [Sentence-Transformer] → [FAISS Index Search] → [LLM (Prompted)] → [JSON Response]
```

## 🛠️ Tech Stack

- **API**: FastAPI
- **LLM**: OpenAI GPT-4
- **Vector DB**: FAISS
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Document Processing**: PyPDF2, python-docx, BeautifulSoup4
- **Deployment**: Render

## 📦 Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your OpenAI API key and other settings
```

3. Run the application:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🔧 Environment Variables

Create a `.env` file with:

```
OPENAI_API_KEY=your_openai_api_key_here
API_SECRET_KEY=your_secret_key_for_jwt
BEARER_TOKEN=your_bearer_token_for_api_access
LOG_LEVEL=INFO
```

## 📝 API Usage

### POST /hackrx/run

**Headers:**

```
Authorization: Bearer your_bearer_token
Content-Type: application/json
```

**Request Body:**

```json
{
  "documents": [
    {
      "type": "url",
      "content": "https://example.com/policy.pdf"
    },
    {
      "type": "text",
      "content": "Your policy document text here..."
    }
  ],
  "questions": [
    "What is the coverage limit for medical expenses?",
    "What are the exclusions in this policy?"
  ]
}
```

**Response:**

```json
{
  "answers": [
    {
      "question": "What is the coverage limit for medical expenses?",
      "answer": "The coverage limit for medical expenses is $100,000 per incident as specified in Section 3.2.1.",
      "confidence": 0.95,
      "source_chunks": ["Section 3.2.1: Medical expense coverage..."]
    }
  ],
  "processing_time": 2.3,
  "status": "success"
}
```

## 🚀 Deployment on Render

1. Connect your GitHub repository to Render
2. Set environment variables in Render dashboard
3. Use the following build/start commands:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 📊 Performance

- Response time: < 30 seconds
- Supports multiple document formats
- Optimized for insurance and legal document analysis
- Accurate clause extraction and matching

## 🧠 LLM Prompting Strategy

The system uses specialized prompts designed for:

- Precise policy/contract language reading
- Context-matched answer extraction
- Factual responses without hallucination
- Concise and clear communication

## 🔒 Security

- Bearer token authentication
- Input validation and sanitization
- Rate limiting ready
- Secure environment variable handling
