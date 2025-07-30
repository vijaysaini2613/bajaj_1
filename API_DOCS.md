# API Documentation

## Authentication

All requests to the `/hackrx/run` endpoint require Bearer token authentication.

```bash
curl -X POST "https://your-app.onrender.com/hackrx/run" \
  -H "Authorization: Bearer your_bearer_token" \
  -H "Content-Type: application/json" \
  -d @request.json
```

## Request Format

### Documents

The `documents` array supports multiple document types:

#### Text Document

```json
{
  "type": "text",
  "content": "Your document text content here..."
}
```

#### URL Document (PDF, DOCX, HTML)

```json
{
  "type": "url",
  "content": "https://example.com/document.pdf"
}
```

#### Base64 Encoded PDF

```json
{
  "type": "pdf",
  "content": "base64_encoded_pdf_content_here"
}
```

#### Base64 Encoded DOCX

```json
{
  "type": "docx",
  "content": "base64_encoded_docx_content_here"
}
```

### Questions

The `questions` array contains the questions you want answered:

```json
{
  "questions": [
    "What is the coverage limit for medical expenses?",
    "What are the policy exclusions?",
    "What is the deductible amount?"
  ]
}
```

## Response Format

```json
{
  "answers": [
    {
      "question": "What is the coverage limit for medical expenses?",
      "answer": "The coverage limit for medical expenses is $100,000 per incident as specified in Section 3.2.1.",
      "confidence": 0.95,
      "source_chunks": [
        "Section 3.2.1: Medical expense coverage shall not exceed $100,000 per incident..."
      ],
      "reasoning": "Found explicit coverage limit in Section 3.2.1"
    }
  ],
  "processing_time": 2.3,
  "status": "success",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Error Responses

### 401 Unauthorized

```json
{
  "detail": "Invalid authentication token"
}
```

### 422 Validation Error

```json
{
  "detail": [
    {
      "loc": ["body", "documents"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error

```json
{
  "error": "Internal server error",
  "detail": "Error description",
  "timestamp": "2024-01-01T12:00:00Z",
  "status_code": 500
}
```

## Example Usage

### Python Example

```python
import requests
import json

url = "https://your-app.onrender.com/hackrx/run"
headers = {
    "Authorization": "Bearer your_bearer_token",
    "Content-Type": "application/json"
}

data = {
    "documents": [
        {
            "type": "url",
            "content": "https://example.com/insurance-policy.pdf"
        }
    ],
    "questions": [
        "What is the maximum coverage amount?",
        "What are the exclusions?"
    ]
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

### JavaScript Example

```javascript
const response = await fetch("https://your-app.onrender.com/hackrx/run", {
  method: "POST",
  headers: {
    Authorization: "Bearer your_bearer_token",
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    documents: [
      {
        type: "text",
        content: "Your insurance policy text here...",
      },
    ],
    questions: ["What is the coverage limit?", "What are the exclusions?"],
  }),
});

const result = await response.json();
console.log(result);
```

## Rate Limits

- Maximum 10 documents per request
- Maximum 20 questions per request
- Maximum 10MB total content size per request
- Processing timeout: 30 seconds

## Best Practices

1. **Document Quality**: Ensure documents are clear and well-formatted
2. **Question Specificity**: Ask specific, clear questions for better results
3. **Context Length**: Keep documents reasonably sized for optimal processing
4. **Authentication**: Keep your bearer token secure and rotate regularly
