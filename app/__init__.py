import os
import sys
import logging

def get_application_path():
    """Get the base path for the application, works both for dev and packaged versions"""
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle
        return os.path.dirname(sys.executable)
    else:
        # If the application is run from a Python interpreter
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def setup_logging():
    base_path = get_application_path()
    logs_dir = os.path.join(base_path, 'logs')
    
    # Create logs directory if it doesn't exist
    os.makedirs(logs_dir, exist_ok=True)
    
    # Setup logging with the correct path
    log_file = os.path.join(logs_dir, 'app.log')
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

# Call setup_logging at application startup
setup_logging()
