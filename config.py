import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application configuration settings"""
    
    # API Configuration
    API_SECRET_KEY: str = os.getenv("API_SECRET_KEY", "your-secret-key-here")
    BEARER_TOKEN: str = os.getenv("BEARER_TOKEN", "your-bearer-token-here")
    
    # Google Gemini Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")  # Now used for Gemini API key
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gemini-pro")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "500"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.1"))
    
    # Embedding Model Configuration
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-mpnet-base-v2")
    
    # Text Processing Configuration
    MAX_CHUNK_SIZE: int = int(os.getenv("MAX_CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    TOP_K_RESULTS: int = int(os.getenv("TOP_K_RESULTS", "5"))
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Request Limits
    MAX_DOCUMENTS: int = int(os.getenv("MAX_DOCUMENTS", "10"))
    MAX_QUESTIONS: int = int(os.getenv("MAX_QUESTIONS", "20"))
    MAX_CONTENT_SIZE: int = int(os.getenv("MAX_CONTENT_SIZE", "10485760"))  # 10MB
    
    # CORS Configuration
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    
    def validate(self) -> bool:
        """Validate configuration settings"""
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
        
        if not self.BEARER_TOKEN or self.BEARER_TOKEN == "your-bearer-token-here":
            raise ValueError("BEARER_TOKEN must be set to a secure value")
        
        return True

# Global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get application settings"""
    return settings
