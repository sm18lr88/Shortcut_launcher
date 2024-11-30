# app/error_logger.py

import logging
import os

def setup_error_logging():
    """
    Sets up additional error-specific logging handlers if needed.
    This complements the basic logging setup in __init__.py
    """
    error_logger = logging.getLogger('error_logger')
    error_logger.setLevel(logging.ERROR)
    
    # Create logs directory if it doesn't exist
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create a file handler specifically for errors
    error_file_handler = logging.FileHandler(os.path.join(log_dir, 'error.log'))
    error_file_handler.setLevel(logging.ERROR)
    
    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    error_file_handler.setFormatter(formatter)
    
    # Add the handler to the logger
    error_logger.addHandler(error_file_handler)
    
    return error_logger
