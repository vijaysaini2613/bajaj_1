# Render Deployment Guide

## Build and Start Commands

### Build Command
```bash
pip install --no-cache-dir -r requirements-ultra.txt
```

### Start Command
```bash
uvicorn main_minimal:app --host 0.0.0.0 --port $PORT
```

## Manual Setup on Render

### 1. Connect Your Repository
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository: `vijaysaini2613/bajaj_1`
4. Select the `main` branch

### 2. Configure Service Settings
- **Name**: `document-qa-system`
- **Region**: Choose your preferred region
- **Branch**: `main`
- **Runtime**: `Python 3`
- **Build Command**: `pip install --no-cache-dir -r requirements-ultra.txt`
- **Start Command**: `uvicorn main_minimal:app --host 0.0.0.0 --port $PORT`

### 3. Set Environment Variables
Go to the "Environment" tab and add these variables:

**Required:**
- `GEMINI_API_KEY`: Your Google Gemini API key
- `BEARER_TOKEN`: A secure token for API authentication (e.g., `your-secure-token-123`)

**Optional (with defaults):**
- `ENVIRONMENT`: `production`
- `MAX_CHUNK_SIZE`: `2000`
- `TOP_K_RESULTS`: `5`

### 4. Deploy
1. Click "Create Web Service"
2. Wait for the build to complete (5-10 minutes)
3. Your service will be available at: `https://document-qa-system-XXXX.onrender.com`

## Testing Your Deployment

### 1. Health Check
Visit: `https://your-app-url.onrender.com/health`
Should return: `{"status": "healthy"}`

### 2. Web Interface
Visit: `https://your-app-url.onrender.com/`
You should see the document Q&A interface

### 3. Upload and Test
1. Upload your insurance PDF
2. Ask questions like "What is covered under this policy?"
3. Verify you get accurate responses

## Troubleshooting

### Build Fails
- Check that `requirements-ultra.txt` only contains pure Python packages
- Verify Python version is set to 3.11.9 in `runtime.txt`

### App Won't Start
- Ensure `main_minimal.py` exists and imports correctly
- Check logs for any missing environment variables

### API Errors
- Verify `GEMINI_API_KEY` is set correctly
- Check that `BEARER_TOKEN` matches what you're using in requests

## File Structure Used in Deployment

```
├── main_minimal.py              # Minimal FastAPI app
├── requirements-ultra.txt       # Ultra-minimal dependencies
├── runtime.txt                 # Python version
├── render.yaml                 # Render configuration
├── app/
│   ├── services/
│   │   ├── simple_document_processor.py  # Basic PDF processing
│   │   ├── llm_service.py               # Gemini integration
│   │   ├── basic_text_search.py         # Fallback search
│   │   └── vector_search.py             # FAISS (if available)
│   └── models/
│       └── simple_models.py             # Custom model classes
└── static/                              # Web interface files
```

## Features Available in Minimal Deployment

✅ PDF document upload and processing  
✅ Google Gemini AI for question answering  
✅ Web interface for easy interaction  
✅ API endpoints for programmatic access  
✅ Vector search with multiple fallbacks  
✅ Authentication with bearer tokens  
✅ Health monitoring endpoint  

## Performance Notes

- **Cold starts**: First request may take 10-15 seconds
- **Concurrent users**: Starter plan supports limited concurrent requests
- **Vector search**: Falls back to basic text search if FAISS fails
- **Memory usage**: Optimized for minimal resource consumption
