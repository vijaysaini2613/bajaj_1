#!/usr/bin/env python3
"""
Development server script for the Document Q&A System
"""

import uvicorn
import os
from main import app

if __name__ == "__main__":
    # Development server configuration
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True
    )
