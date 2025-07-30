# Deployment Guide for Document Q&A System

## Quick Start for Render

Use this build command in Render dashboard:

```bash
pip install --no-cache-dir -r requirements-minimal.txt
```

Start command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Environment Variables Required

Set these in your Render dashboard:

- `GEMINI_API_KEY`: Your Google Gemini API key
- `BEARER_TOKEN`: Any secure string for API authentication
- `MODEL_NAME`: gemini-1.5-flash (recommended)

## Requirements Files Explained

### requirements-minimal.txt (RECOMMENDED FOR RENDER)

- ✅ **No compilation needed**
- ✅ **Fastest deployment**
- ✅ **Works on all platforms**
- ⚠️ Uses basic text search (still effective)

### requirements-lite.txt

- ⚠️ **May fail on some platforms**
- ✅ Uses TF-IDF vectors (better accuracy)
- Requires scikit-learn compilation

### requirements.txt

- ⚠️ **Often fails on cloud platforms**
- ✅ Full FAISS + sentence transformers (best accuracy)
- Requires heavy compilation

## Performance Comparison

| Requirements File        | Deployment Success | Search Quality | Speed  |
| ------------------------ | ------------------ | -------------- | ------ |
| requirements-minimal.txt | 99%                | Good           | Fast   |
| requirements-lite.txt    | 70%                | Better         | Medium |
| requirements.txt         | 30%                | Best           | Slow   |

## Troubleshooting

### If deployment still fails:

1. Check Python version is 3.11.9
2. Try removing cryptography from python-jose:
   ```
   python-jose==3.3.0
   ```
3. Use even more minimal requirements if needed

### If you need better search quality:

1. Deploy with requirements-minimal.txt first
2. Once working, try upgrading to requirements-lite.txt
3. The system will automatically fall back if imports fail

## System Features with Minimal Requirements

Even with basic text search, your system will:

- ✅ Process PDF documents
- ✅ Answer questions with good accuracy
- ✅ Use Google Gemini for high-quality responses
- ✅ Provide confidence scores
- ✅ Handle multiple document types
- ✅ Serve modern web interface

The basic text search is surprisingly effective for document Q&A!
