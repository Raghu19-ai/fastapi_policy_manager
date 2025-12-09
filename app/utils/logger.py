import logging
import sys
import json
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
from typing import Optional, Dict, Any

# Configure logging directory
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# Log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

class JSONFormatter(logging.Formatter):
    """Custom formatter to output logs in JSON format"""
    
    def format(self, record):
        log_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'name': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)
            
        # Add any extra attributes
        if hasattr(record, 'extra'):
            log_record.update(record.extra)
            
        return json.dumps(log_record)

def setup_logger(name: str, log_level: str = 'INFO') -> logging.Logger:
    """
    Setup a logger with the specified name and log level.
    
    Args:
        name: Name of the logger (usually __name__)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Don't propagate to parent loggers
    logger.propagate = False
    
    # Return existing logger if already configured
    if logger.handlers:
        return logger
    
    # Create formatters
    json_formatter = JSONFormatter()
    console_formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
    
    # Console handler (always at INFO level)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel('INFO')
    console_handler.setFormatter(console_formatter)
    
    # File handler (JSON format, rotates when reaches 5MB, keeps 5 backups)
    log_file = os.path.join(LOG_DIR, f"{name}.log")
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5*1024*1024, backupCount=5, encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(json_formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

def log_request_response(
    logger: logging.Logger,
    request_id: str,
    method: str,
    url: str,
    status_code: int,
    request_body: Optional[Dict[str, Any]] = None,
    response_body: Optional[Dict[str, Any]] = None,
    processing_time: Optional[float] = None,
    **extra: Any
) -> None:
    """
    Log HTTP request and response details in a structured way.
    
    Args:
        logger: Logger instance
        request_id: Unique request ID
        method: HTTP method (GET, POST, etc.)
        url: Request URL
        status_code: HTTP status code
        request_body: Request body (if any)
        response_body: Response body (if any)
        processing_time: Request processing time in seconds
        **extra: Additional fields to include in the log
    """
    log_data = {
        'request_id': request_id,
        'method': method,
        'url': url,
        'status_code': status_code,
        'processing_time_seconds': processing_time,
        **extra
    }
    
    if request_body is not None:
        log_data['request_body'] = request_body
    
    if response_body is not None:
        log_data['response_body'] = response_body
    
    # Log at INFO for successful requests, ERROR for server errors, WARNING for client errors
    if status_code >= 500:
        logger.error('Request processed with server error', extra=log_data)
    elif status_code >= 400:
        logger.warning('Request processed with client error', extra=log_data)
    else:
        logger.info('Request processed successfully', extra=log_data)

# Create default logger instance
logger = setup_logger(__name__)

# Example usage:
if __name__ == "__main__":
    # Example of using the logger
    logger.info("Logger initialized successfully")
    logger.debug("This is a debug message")
    logger.warning("This is a warning message")
    
    try:
        # Simulate an error
        1 / 0
    except Exception as e:
        logger.error("An error occurred", exc_info=True)
    
    # Example of request/response logging
    log_request_response(
        logger=logger,
        request_id="req_123",
        method="POST",
        url="/api/example",
        status_code=200,
        request_body={"key": "value"},
        response_body={"status": "success"},
        processing_time=0.123
    )
