# Environment Setup for Render

## Required Environment Variables

You MUST set these environment variables in your Render dashboard for the application to work:

### 1. GEMINI_API_KEY (REQUIRED)

- Go to Render Dashboard → Your Service → Environment
- Add: `GEMINI_API_KEY` = `YOUR_ACTUAL_GEMINI_API_KEY`
- This is your Google AI Studio API key

### 2. BEARER_TOKEN (REQUIRED for API security)

- Add: `BEARER_TOKEN` = `your-secure-token-123`
- Use a strong, random token for security

### Optional Environment Variables (have defaults):

- `ENVIRONMENT` = `production` (already set)
- `MAX_CHUNK_SIZE` = `2000` (already set)
- `TOP_K_RESULTS` = `5` (already set)

## How to Set Environment Variables in Render:

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Select your `document-qa-system` service
3. Click on "Environment" tab
4. Click "Add Environment Variable"
5. Add the required variables above

## Testing After Setup:

1. **Health Check**: Visit `https://your-app.onrender.com/health`

   - Should return: `{"status": "healthy", "vector_search_type": "...", "environment": "production"}`

2. **Web Interface**: Visit `https://your-app.onrender.com/`

   - Should show the document upload interface

3. **Upload Test**: Try uploading a PDF and asking questions

## Important Notes:

- The app will start successfully even without GEMINI_API_KEY set
- The LLM service will only initialize when you first try to ask a question
- If GEMINI_API_KEY is missing, you'll get a clear error message when trying to use Q&A functionality
- The health endpoint and web interface will work regardless

## Troubleshooting:

### "LLM service not available" error:

- Check that GEMINI_API_KEY is set correctly in Render environment variables
- Verify the API key is valid in Google AI Studio

### "Not authenticated" error:

- Ensure BEARER_TOKEN is set
- Use the same token in your API requests: `Authorization: Bearer your-secure-token-123`

### App won't start:

- Check build logs for dependency issues
- Verify Python version is 3.11.9 in runtime.txt
