<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Document Q&A System - Copilot Instructions

This is a FastAPI-based document Q&A system designed for insurance policy and legal document analysis.

## Project Context

- **Purpose**: Process insurance policies, legal documents, and contracts to provide accurate Q&A capabilities
- **Architecture**: FastAPI + FAISS + OpenAI GPT-4 + Sentence Transformers
- **Deployment**: Render hosting with production-ready configuration

## Code Guidelines

- Follow FastAPI best practices for async/await patterns
- Use Pydantic models for request/response validation
- Implement proper error handling with detailed logging
- Use type hints throughout the codebase
- Follow security best practices for API authentication

## Domain-Specific Requirements

- Focus on insurance and legal document terminology
- Ensure accurate clause extraction and context matching
- Avoid hallucination in LLM responses
- Provide source attribution for answers
- Maintain response times under 30 seconds

## File Structure

- `main.py`: FastAPI application entry point
- `app/`: Core application modules
- `models/`: Pydantic data models
- `services/`: Business logic (document processing, vector search, LLM)
- `utils/`: Utility functions
- `config.py`: Configuration management

## API Standards

- Use RESTful conventions
- Implement proper HTTP status codes
- Include comprehensive error messages
- Support Bearer token authentication
- Return JSON responses with consistent structure
