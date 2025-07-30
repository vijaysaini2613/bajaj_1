# Deployment Guide

## Quick Start for Render Deployment

### 1. Prepare Your Repository

1. Push this code to a GitHub repository
2. Connect your GitHub account to Render
3. Create a new Web Service on Render

### 2. Render Configuration

**Service Type**: Web Service
**Build Command**: `pip install -r requirements.txt`
**Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
**Python Version**: 3.11.0 (specified in runtime.txt)

### 3. Environment Variables

Set the following environment variables in your Render dashboard:

#### Required Variables

```
OPENAI_API_KEY=your_openai_api_key_here
BEARER_TOKEN=your_secure_bearer_token_here
API_SECRET_KEY=your_secret_key_for_jwt_tokens
```

#### Optional Variables (with defaults)

```
ENVIRONMENT=production
LOG_LEVEL=INFO
MODEL_NAME=gpt-4
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
MAX_CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
MAX_DOCUMENTS=10
MAX_QUESTIONS=20
```

### 4. Health Check

Render will automatically check the `/health` endpoint to ensure your service is running properly.

### 5. Domain Setup

Your service will be available at: `https://your-service-name.onrender.com`

## Local Development

### 1. Setup Environment

```bash
# Clone the repository
git clone your-repo-url
cd bajaj_1

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
```

### 2. Configure Environment Variables

Edit `.env` file with your actual values:

```env
OPENAI_API_KEY=your_actual_openai_api_key
BEARER_TOKEN=your_secure_bearer_token
API_SECRET_KEY=your_secret_key
LOG_LEVEL=DEBUG
ENVIRONMENT=development
```

### 3. Run Development Server

```bash
# Method 1: Using the dev script
python dev_server.py

# Method 2: Using uvicorn directly
uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Method 3: Using VS Code task
# Open VS Code and run the "Install Dependencies and Run Development Server" task
```

### 4. Test the API

Visit:

- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Main endpoint: http://localhost:8000/hackrx/run (requires authentication)

## Testing

```bash
# Install test dependencies
pip install pytest httpx

# Run tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_api.py -v
```

## Production Checklist

### Security

- [ ] Set secure BEARER_TOKEN (not the default)
- [ ] Set secure API_SECRET_KEY
- [ ] Valid OPENAI_API_KEY configured
- [ ] CORS origins configured for production
- [ ] HTTPS enabled (automatic with Render)

### Performance

- [ ] Appropriate server resources allocated
- [ ] Embedding model loads successfully
- [ ] Response times under 30 seconds
- [ ] Error handling tested

### Monitoring

- [ ] Health check endpoint working
- [ ] Logging configured appropriately
- [ ] Error tracking in place

## Troubleshooting

### Common Issues

**1. "Import could not be resolved" errors**

- Solution: Ensure all packages are installed with `pip install -r requirements.txt`

**2. "Invalid authentication token"**

- Solution: Check that BEARER_TOKEN is set and matches your request headers

**3. "OpenAI API error"**

- Solution: Verify OPENAI_API_KEY is valid and has sufficient credits

**4. "FAISS index creation failed"**

- Solution: Ensure sentence-transformers model downloads successfully

**5. "PDF processing error"**

- Solution: Check PDF is not corrupted and is text-based (not image-only)

### Logs and Debugging

**Local Development:**

- Logs are output to console and `logs/app.log`
- Set `LOG_LEVEL=DEBUG` for detailed logging

**Production (Render):**

- View logs in Render dashboard
- Use `LOG_LEVEL=INFO` for production

### Performance Optimization

**For better response times:**

1. Use GPU-enabled hosting for faster embeddings (if available)
2. Cache embedding models locally
3. Implement request queuing for high load
4. Use Redis for caching frequent queries

**For cost optimization:**

1. Use gpt-3.5-turbo instead of gpt-4 (set MODEL_NAME=gpt-3.5-turbo)
2. Reduce MAX_TOKENS for shorter responses
3. Implement request rate limiting

## API Usage Examples

See `API_DOCS.md` for detailed API documentation and usage examples.

## Support

For issues and questions:

1. Check the logs for error details
2. Verify environment variables are set correctly
3. Test with simple text documents first
4. Ensure your OpenAI API key has sufficient credits
