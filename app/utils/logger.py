import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

def setup_logger(name: str, level: str = None) -> logging.Logger:
    """
    Set up a logger with both file and console handlers
    
    Args:
        name: Logger name
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    if level is None:
        level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, level))
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (rotating)
    try:
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        file_handler = RotatingFileHandler(
            'logs/app.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(getattr(logging, level))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        # If file logging fails, continue with console only
        logger.warning(f"Could not set up file logging: {e}")
    
    return logger

def log_request_response(logger: logging.Logger, request_data: dict, response_data: dict, processing_time: float):
    """
    Log request and response data for debugging and monitoring
    
    Args:
        logger: Logger instance
        request_data: Request data dictionary
        response_data: Response data dictionary
        processing_time: Processing time in seconds
    """
    logger.info(f"Request processed in {processing_time:.2f}s")
    logger.debug(f"Request: {request_data}")
    logger.debug(f"Response: {response_data}")

def log_error(logger: logging.Logger, error: Exception, context: str = ""):
    """
    Log error with context information
    
    Args:
        logger: Logger instance
        error: Exception instance
        context: Additional context string
    """
    error_msg = f"Error in {context}: {str(error)}" if context else f"Error: {str(error)}"
    logger.error(error_msg, exc_info=True)
